import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import functions
from uuid import uuid4
import asyncio
import threading
import re

# === Flask-приложение ===
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Для сессий
# Разрешаем кросс-доменные cookies (нужно для Tilda → ngrok HTTPS)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# === Business Configuration ===
BUSINESS_NAME = os.getenv('BUSINESS_NAME', 'Наше заведение')

# === Память для Telegram-чатов (как в веб-виджете) ===
tg_chat_history = {}
tg_chat_booking = {}

# === Инициализация Telegram Application ===
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# === Запуск Telegram Application в отдельном asyncio-цикле ===
telegram_loop = asyncio.new_event_loop()

def _start_telegram_app():
    asyncio.set_event_loop(telegram_loop)
    telegram_loop.run_until_complete(telegram_app.initialize())
    telegram_loop.run_until_complete(telegram_app.start())
    telegram_loop.run_forever()

threading.Thread(target=_start_telegram_app, daemon=True).start()

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Здравствуйте! Я ассистент {BUSINESS_NAME}. Хотите расскажу подробнее об услугах или помогу записаться?",
        reply_markup=ReplyKeyboardRemove()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (update.message.text or '').strip()

    # Инициализация структур
    chat_history = tg_chat_history.get(chat_id, [])
    booking = tg_chat_booking.get(chat_id, {
        'Имя': '',
        'Телефон': '',
        'Желаемая услуга': '',
        'Дата и время желаемой записи': '',
        'Категория мастера': '',
        'Комментарий/Пожелания': ''
    })

    # Приветствия: просто повторяем вступление
    if text.lower() in ['привет', 'здравствуйте', 'добрый день', 'доброе утро', 'добрый вечер']:
        await update.message.reply_text(
            f"Здравствуйте! Я ассистент {BUSINESS_NAME}. Хотите расскажу подробнее об услугах или помогу записаться?"
        )
        return

    # Если это чисто информационный вопрос (без намерения записаться) — отвечаем кратко и не запускаем сбор данных
    info_triggers = ['до скольки', 'режим работы', 'сколько стоит', 'цена', 'стоимость', 'адрес', 'где находит', 'как добраться']
    if any(k in text.lower() for k in info_triggers) and not any(t in text.lower() for t in ['запис', 'оформить', 'хочу прийти']):
        ans = functions.get_openai_info_response(text)
        await update.message.reply_text(ans)
        await update.message.reply_text("Могу ли я ещё чем-то помочь или вы готовы записаться?")
        return

    # Добавляем сообщение пользователя в историю
    chat_history.append({"role": "user", "content": text})
    chat_history = chat_history[-10:]

    # Пробуем извлечь имя/телефон/услугу из текста
    def extract_from_text(t: str):
        updates = {}
        m = re.search(r"(\+?\d[\d\s\-()]{9,})", t)
        if m and not booking['Телефон']:
            phone = re.sub(r"[^\d\+]", "", m.group(1))
            updates['Телефон'] = phone
        m = re.search(r"(?:меня зовут|моё имя|мое имя)\s+([А-ЯЁA-Z][а-яёa-z]+)", t, re.IGNORECASE)
        if m and not booking['Имя']:
            updates['Имя'] = m.group(1).strip().title()
        return updates

    upd = extract_from_text(text)
    if upd:
        booking.update(upd)

    # Готовим системную сводку прогресса
    known = [f"{k}: {v}" for k, v in booking.items() if v]
    missing = [k for k, v in booking.items() if not v]
    progress_note = (
        "Контекст бронирования пользователя. Уже известные данные: " + (", ".join(known) if known else "нет") +
        ". Недостающие поля по порядку: " + ", ".join(missing) +
        ". Спрашивай ТОЛЬКО следующий недостающий пункт и не переспроси уже известные. Если все поля собраны — выведи ТОЛЬКО JSON согласно инструкции."
    )

    # Сообщения для модели (как в виджете)
    messages = [
        {"role": "system", "content": functions.PROMPT},
        {"role": "system", "content": progress_note}
    ] + chat_history

    answer = functions.get_openai_response_with_history(messages)
    # Если ассистент вернул JSON без телефона — мягко просим телефон и выходим
    if functions.json_missing_phone(answer):
        await update.message.reply_text("Пожалуйста, укажите номер телефона для связи (например, +79991234567).")
        return

    # Попытка извлечь JSON, сохранить и уведомить
    booking_json = functions.extract_booking_json(answer)
    saved = False
    if booking_json:
        try:
            functions.save_booking_data(booking_json)
            saved = True
        except Exception:
            saved = False

    # Обновляем историю и память
    chat_history.append({"role": "assistant", "content": answer})
    tg_chat_history[chat_id] = chat_history[-10:]
    tg_chat_booking[chat_id] = {} if saved else booking

    # Скрываем JSON из ответа перед отправкой пользователю
    if saved:
        confirm = (
            "✅ Ваша запись сохранена! Мы свяжемся с вами для подтверждения."
        )
        await update.message.reply_text(confirm, reply_markup=ReplyKeyboardRemove())
    else:
        visible_answer = functions.strip_booking_json(answer)
        await update.message.reply_text(visible_answer or "", reply_markup=ReplyKeyboardRemove())

# === Отмена ===
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Запись отменена.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

telegram_app.add_handler(CommandHandler('start', start))
telegram_app.add_handler(MessageHandler(filters.Regex("(?i)^(привет|здравствуйте)$"), start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# === Flask route: Telegram webhook ===
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    # Отправляем обработку апдейта в фоновый цикл Telegram-приложения
    telegram_loop.call_soon_threadsafe(asyncio.create_task, telegram_app.process_update(update))
    return 'ok'

# === Flask route: Web chat widget (Tilda) с историей диалога ===
# Храним историю в session['chat_history'] (до 10 сообщений)
@app.route('/widget', methods=['POST'])
def widget():
    # Генерируем уникальный session id, если его нет
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())
    # Получаем историю диалога
    chat_history = session.get('chat_history', [])
    data = request.json
    user_message = data.get('message', '')
    # Авто-приветствие для новой сессии
    if not session.get('greeted'):
        session['greeted'] = True
        greeting = (
            f"Здравствуйте! Я ассистент {BUSINESS_NAME}. "
            "Хотите расскажу подробнее об услугах или помогу записаться?"
        )
        # Сохраним приветствие в истории как ответ ассистента
        chat_history.append({"role": "assistant", "content": greeting})
        session['chat_history'] = chat_history[-10:]
        return jsonify({'answer': greeting, 'saved': False})

    # Если это первое реальное сообщение и это приветствие — тоже отвечаем стандартным приветствием
    if (user_message or '').strip().lower() in ['привет', 'здравствуйте', 'добрый день', 'доброе утро', 'добрый вечер']:
        greeting = (
            f"Здравствуйте! Я ассистент {BUSINESS_NAME}. "
            "Хотите расскажу подробнее об услугах или помогу записаться?"
        )
        chat_history.append({"role": "assistant", "content": greeting})
        session['chat_history'] = chat_history[-10:]
        return jsonify({'answer': greeting, 'saved': False})
    # Инициализируем структуру бронирования
    booking = session.get('booking', {
        'Имя': '',
        'Телефон': '',
        'Желаемая услуга': '',
        'Дата и время желаемой записи': '',
        'Категория мастера': '',
        'Комментарий/Пожелания': ''
    })

    # Добавляем новое сообщение пользователя
    chat_history.append({"role": "user", "content": user_message})

    # Простая попытка извлечь имя/телефон/услугу из фразы
    def extract_from_text(text: str):
        updates = {}
        m = re.search(r"(\+?\d[\d\s\-()]{9,})", text)
        if m and not booking['Телефон']:
            phone = re.sub(r"[^\d\+]", "", m.group(1))
            updates['Телефон'] = phone
        m = re.search(r"(?:меня зовут|моё имя|мое имя)\s+([А-ЯЁA-Z][а-яёa-z]+)", text, re.IGNORECASE)
        if m and not booking['Имя']:
            updates['Имя'] = m.group(1).strip().title()
        return updates

    upd = extract_from_text(user_message)
    if upd:
        booking.update(upd)
    session['booking'] = booking
    # Обрезаем историю до 10 последних сообщений
    chat_history = chat_history[-10:]
    # Формируем системное сообщение с прогрессом
    known = [f"{k}: {v}" for k, v in booking.items() if v]
    missing = [k for k, v in booking.items() if not v]
    progress_note = (
        "Контекст бронирования пользователя. Уже известные данные: " + (", ".join(known) if known else "нет") +
        ". Недостающие поля по порядку: " + ", ".join(missing) +
        ". Спрашивай ТОЛЬКО следующий недостающий пункт и не переспроси уже известные. Если все поля собраны — выведи ТОЛЬКО JSON согласно инструкции."
    )

    # Формируем messages для OpenAI: системный промпт + прогресс + история
    messages = [
        {"role": "system", "content": functions.PROMPT},
        {"role": "system", "content": progress_note}
    ] + chat_history
    # Получаем ответ от OpenAI
    answer = functions.get_openai_response_with_history(messages)
    # Попытка извлечь JSON заявки и сохранить
    booking = functions.extract_booking_json(answer)
    saved = False
    if booking:
        try:
            functions.save_booking_data(booking)
            saved = True
        except Exception:
            saved = False
    # Добавляем ответ ассистента в историю
    chat_history.append({"role": "assistant", "content": answer})
    chat_history = chat_history[-10:]
    session['chat_history'] = chat_history
    # Если сохранили — сбрасываем накопленные поля
    if saved:
        session['booking'] = {
            'Имя': '',
            'Телефон': '',
            'Желаемая услуга': '',
            'Дата и время желаемой записи': '',
            'Категория мастера': '',
            'Комментарий/Пожелания': ''
        }
    return jsonify({'answer': answer, 'saved': saved})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)