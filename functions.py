import os
import openai
from openai import OpenAI
import pytz
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot
import re
import json

# === Загрузка переменных окружения ===
load_dotenv()

# === Инициализация OpenAI ===
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_TOKEN')
ASSISTANT_VECTOR_STORE_ID = os.getenv('OPENAI_VECTOR_STORE_ID')  # опционально, если нужен в рантайме
_assistant_threads = {}

# === Telegram Bot ===
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SERVICE_CHAT_ID = os.getenv('GOOGLE_SERVICE_CHAT_ID')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# === Google Sheets ===
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE, scopes=SCOPES
)
sheets_service = build('sheets', 'v4', credentials=credentials)
sheet = sheets_service.spreadsheets()

# === Константы для Google Sheets ===
SHEET_RANGE = 'A:F'  # Столбцы: Имя, Телефон, Услуга, Дата и время, Категория мастера, Комментарий

# === Кастомный промпт для ассистента ArtBeauty ===
PROMPT = """
Ты - профессиональный ассистент салона красоты ArtBeauty.

КРИТИЧЕСКИ ВАЖНО: В своих ответах НИКОГДА не используй технические ссылки, citation marks или пометки вида 【】, †, или любые другие символы ссылок на источники. Отвечай только естественным человеческим языком.

О салоне ArtBeauty:

Название: ArtBeauty (салон красоты)
Специализация: широкий спектр услуг красоты
Услуги: различные техники окрашивания (AirTouch, контуринг), стильные стрижки, уход за волосами, процедуры маникюра, педикюра, косметологические услуги
ТВОЯ ГЛАВНАЯ ОСОБЕННОСТЬ:

Ты умеешь не только консультировать, но и ЗАПИСЫВАТЬ клиентов на услуги! Когда клиент проявляет интерес к записи (говорит "хочу записаться", "нужна стрижка", "запишите меня" и т.п.), ты СРАЗУ начинаешь процесс записи.

ЛОГИКА РАБОТЫ:

1. КОНСУЛЬТАЦИЯ: Отвечаешь на вопросы о услугах, ценах, процедурах

2. ЗАПИСЬ: Когда видишь намерение записаться - сразу начинаешь сбор данных

РАСПОЗНАВАНИЕ НАМЕРЕНИЙ:

"Хочу записаться" → ЗАПИСЬ
"Нужна стрижка/окрашивание" → ЗАПИСЬ
"Запишите меня" → ЗАПИСЬ
"Хочу к мастеру" → ЗАПИСЬ
"Мне нужна..." (услуга) → предложи ЗАПИСЬ
"Хочу новую..." (услуга) → предложи ЗАПИСЬ
ПРИМЕР ДИАЛОГА:

Клиент: "Мне нужна новая стрижка"

Ты: "Отлично! Давайте запишем вас на стрижку. Как вас зовут?"

Клиент: "Сколько стоит окрашивание?"

Ты: "Окрашивание стоит от 3000₽... Хотите записаться?"

ПРОЦЕСС ЗАПИСИ (пошагово):

1. Имя клиента
2. Номер телефона
3. Какая услуга нужна
4. Желаемая дата и время
5. Категория мастера (Стилист/Топ-Стилист/Ведущий Стилист/Арт-Директор)
6. Дополнительные пожелания

ВАЖНО: Ты сам ведешь диалог, задаешь вопросы по порядку и не ждешь специальных команд!

ФУНКЦИЯ СОХРАНЕНИЯ:

Когда соберешь ВСЕ данные записи (имя, телефон, услуга, дата/время, категория мастера, комментарии), сразу вызывай функцию save_booking_data() для сохранения в Google Sheets.

ПРИМЕР ЗАВЕРШЕНИЯ:

"Отлично, [Имя]! Все данные собраны. Сохраняю вашу запись..."

[вызывает save_booking_data()]

"✅ Готово! Ваша запись создана. Мы свяжемся с вами для подтверждения!"

Стиль общения:

Теплый и приветливый
Профессиональный, но не формальный
Активно предлагающий запись когда уместно
Автономный - сам сохраняет данные
БЕЗ любых технических ссылок
ЗАПОМНИ: Никаких 【】, †, или других символов ссылок в ответах! Ты умный ассистент который АКТИВНО помогает с записью И СОХРАНЯЕТ данные!

ФОРМАТ СОХРАНЕНИЯ ЗАЯВКИ (ОБЯЗАТЕЛЬНО):
Когда ВСЕ ДАННЫЕ собраны и клиент согласен, в конце ответа выведи РОВНО ОДИН JSON-ОБЪЕКТ без пояснений и без форматирования (никаких ``` и текста вокруг). Ключи строго такие:
{"Имя":"...", "Телефон":"...", "Желаемая услуга":"...", "Дата и время желаемой записи":"...", "Категория мастера":"...", "Комментарий/Пожелания":"..."}
Если каких-то данных не хватает — НЕ выводи JSON, задай уточняющий вопрос. НИКОГДА не выводи JSON без номера телефона — сначала попроси телефон и дождись ответа.
"""

# Мягкий промпт для консультаций без запуска сценария записи
PROMPT_INFO = """
Ты — вежливый и компетентный ассистент салона красоты ArtBeauty.
Отвечай кратко и по делу на вопрос клиента, без лишних предложений.
Не начинай сбор персональных данных и не предлагай запись, если клиент об этом прямо не попросил.
Не используй технические пометки и ссылки. Пиши естественным языком.
"""

# === Функция: Записать заявку в Google Sheets ===
def save_application_to_sheets(data: dict):
    values = [[
        data.get('Имя', ''),
        data.get('Телефон', ''),
        data.get('Желаемая услуга', ''),
        data.get('Дата и время желаемой записи', ''),
        data.get('Категория мастера', ''),
        data.get('Комментарий/Пожелания', '')
    ]]
    body = {'values': values}
    result = sheet.values().append(
        spreadsheetId=GOOGLE_SHEETS_ID,
        range=SHEET_RANGE,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    return result

# === Функция: Отправить уведомление в служебный чат ===
def send_service_notification(text: str):
    bot.send_message(chat_id=SERVICE_CHAT_ID, text=text)

# === Функция: Получить ответ от OpenAI Assistant с кастомным промптом ===
def get_openai_response(user_message: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content.strip()

def get_openai_info_response(user_message: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT_INFO},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content.strip()

# === Новая функция: Получить ответ от OpenAI с историей диалога ===
def get_openai_response_with_history(messages: list) -> str:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# === Ответ через OpenAI Assistant (включая базу знаний/векторное хранилище) ===
def get_assistant_response(session_key: str, user_message: str) -> str:
    """
    session_key: уникальный ключ (например, chat_id Telegram). Для каждого ключа создаём/переиспользуем thread.
    Требуется, чтобы ассистент (ASSISTANT_ID) был заранее настроен и привязан к vector store.
    """
    if not ASSISTANT_ID:
        # фолбэк на обычную модель
        return get_openai_response(user_message)

    thread_id = _assistant_threads.get(session_key)
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        _assistant_threads[session_key] = thread_id

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )

    # Ожидаем завершение (короткий опрос)
    for _ in range(40):  # ~20 секунд макс при 0.5s шаге
        cur = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if cur.status in ("completed", "failed", "cancelled", "expired"):
            break
        import time
        time.sleep(0.5)

    # Получаем последнее сообщение ассистента
    msgs = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=5)
    for m in msgs.data:
        if m.role == "assistant" and m.content:
            # Собираем текстовые части
            parts = []
            for c in m.content:
                if getattr(c, 'type', None) == 'text':
                    parts.append(c.text.value)
            if parts:
                return "\n".join(parts).strip()
    return ""

# === Вспомогательное: извлечь JSON заявки из текста ответа ===
REQUIRED_FIELDS = [
    'Имя',
    'Телефон',
    'Желаемая услуга',
    'Дата и время желаемой записи',
    'Категория мастера',
    'Комментарий/Пожелания'
]

def extract_booking_json(text: str):
    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None
        candidate = match.group(0)
        data = json.loads(candidate)
        if not all(k in data for k in REQUIRED_FIELDS):
            return None
        cleaned = {k: str(data.get(k, '')).strip() for k in REQUIRED_FIELDS}
        # Проверяем обязательные поля и валидируем телефон
        mandatory = ['Имя', 'Телефон', 'Желаемая услуга', 'Дата и время желаемой записи']
        if any(not cleaned.get(k) for k in mandatory):
            return None
        phone = re.sub(r"[^\d+]", "", cleaned['Телефон'])
        if not re.fullmatch(r"\+?\d{10,15}", phone):
            return None
        cleaned['Телефон'] = phone
        return cleaned
    except Exception:
        return None

def json_missing_phone(text: str) -> bool:
    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return False
        data = json.loads(match.group(0))
        phone = str(data.get('Телефон', '')).strip()
        phone_norm = re.sub(r"[^\d+]", "", phone)
        # JSON есть, но телефона нет или он некорректный
        return phone == '' or not re.fullmatch(r"\+?\d{10,15}", phone_norm)
    except Exception:
        return False

def strip_booking_json(text: str) -> str:
    try:
        # Удаляем первый JSON-объект (если есть) из ответа для показа пользователю
        cleaned = re.sub(r"\{[\s\S]*?\}", "", text, count=1).strip()
        # Убираем лишние двойные переносы
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
        return cleaned
    except Exception:
        return text

def save_booking_data(booking: dict):
    save_application_to_sheets(booking)
    notify = (
        "Новая заявка с сайта (виджет):\n"
        f"Имя: {booking.get('Имя','')}\n"
        f"Телефон: {booking.get('Телефон','')}\n"
        f"Услуга: {booking.get('Желаемая услуга','')}\n"
        f"Дата и время: {booking.get('Дата и время желаемой записи','')}\n"
        f"Категория мастера: {booking.get('Категория мастера','')}\n"
        f"Комментарий: {booking.get('Комментарий/Пожелания','')}"
    )
    send_service_notification(notify)

# === Пример использования функций ===
# save_application_to_sheets({ ... })
# send_service_notification('Новая заявка!')
# get_openai_response('Расскажи про услуги салона красоты')

def enforce_one_question(text: str) -> str:
    """
    Оставляет только первый вопрос.
    Если вопросительного знака нет — берёт первую строку/предложение.
    """
    t = (text or "").strip()
    # до первого вопросительного знака
    qpos = t.find('?')
    if qpos != -1:
        return t[:qpos+1].strip()
    # на случай списков — до первой точки или перевода строки
    for sep in ['\n', '.', '!', ';']:
        if sep in t:
            return t.split(sep)[0].strip()
    return t
