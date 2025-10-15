# ArtBeauty Booking Bot

Телеграм-бот и веб-виджет для записи клиентов в салон красоты с интеграцией OpenAI Assistant, Google Sheets и Tilda.

## 🎯 Возможности

- **Телеграм-бот**: Консультации и запись на услуги через Telegram
- **Веб-виджет**: Интеграция чата на сайт Tilda
- **AI-ассистент**: Использует OpenAI GPT для диалогов и базу знаний через Vector Store
- **Google Sheets**: Автоматическое сохранение заявок
- **Уведомления**: Отправка новых записей в служебный Telegram-чат

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- OpenAI API ключ + настроенный Assistant
- Google Cloud Service Account с доступом к Google Sheets API
- Ngrok (для локальной разработки) или сервер с HTTPS

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/artbeauty-bot.git
cd artbeauty-bot
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и заполните все необходимые ключи:

```bash
# Flask
FLASK_SECRET_KEY=your_random_secret_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# OpenAI
OPENAI_API_KEY=sk-proj-...
OPENAI_ASSISTANT_TOKEN=asst_...
OPENAI_VECTOR_STORE_ID=vs_... (опционально)

# Google Sheets
GOOGLE_SHEETS_ID=1YL3vdLFKCs8oZ7eubvjnbWx...

# Service Chat
GOOGLE_SERVICE_CHAT_ID=-1002345678901
```

### 5. Настройка Google Sheets API

#### Создание Service Account:

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите **Google Sheets API**:
   - APIs & Services → Library → Google Sheets API → Enable
4. Создайте Service Account:
   - APIs & Services → Credentials → Create Credentials → Service Account
   - Заполните название и описание
   - Скачайте JSON-ключ
5. Переименуйте скачанный файл в `credentials.json` и поместите в корень проекта

#### Настройка доступа к таблице:

1. Откройте вашу Google Таблицу
2. Нажмите "Поделиться"
3. Добавьте email вашего Service Account (из `credentials.json`, поле `client_email`)
4. Дайте права "Редактор"
5. Скопируйте ID таблицы из URL (между `/d/` и `/edit`):
   ```
   https://docs.google.com/spreadsheets/d/[ВОТ_ЭТОТ_ID]/edit
   ```
6. Вставьте ID в `.env` как `GOOGLE_SHEETS_ID`

### 6. Настройка Telegram Bot

#### Создание бота:

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям (название и username бота)
4. Скопируйте полученный токен в `.env` как `TELEGRAM_BOT_TOKEN`

#### Настройка служебного чата:

1. Создайте группу/канал для уведомлений о новых записях
2. Добавьте вашего бота в эту группу
3. Отправьте любое сообщение в группу
4. Получите chat_id группы:
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
5. Найдите `"chat":{"id":-1002345...}` в ответе
6. Скопируйте ID в `.env` как `GOOGLE_SERVICE_CHAT_ID`

### 7. Настройка OpenAI Assistant

#### Создание Assistant:

1. Перейдите в [OpenAI Platform](https://platform.openai.com/)
2. Откройте раздел **Assistants**
3. Создайте нового Assistant:
   - **Name**: ArtBeauty Assistant
   - **Model**: gpt-4-turbo или gpt-3.5-turbo
   - **Instructions**: Скопируйте промпт из `functions.py` (переменная `PROMPT`)
4. Скопируйте Assistant ID (начинается с `asst_...`) в `.env`

#### Создание Vector Store (опционально):

1. В разделе **Storage** создайте Vector Store
2. Загрузите файлы с информацией о салоне (прайсы, описания услуг, FAQ)
3. Привяжите Vector Store к Assistant
4. Скопируйте ID в `.env` как `OPENAI_VECTOR_STORE_ID`

### 8. Запуск через Ngrok (локальная разработка)

Ngrok нужен для получения HTTPS URL, который требуется для Telegram webhook и Tilda.

#### Установка Ngrok:

1. Скачайте с [ngrok.com](https://ngrok.com/download)
2. Зарегистрируйтесь и получите authtoken
3. Настройте:
   ```bash
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

#### Запуск приложения:

Терминал 1 - Flask приложение:
```bash
python main.py
```

Терминал 2 - Ngrok туннель:
```bash
ngrok http 5000
```

Скопируйте HTTPS URL из Ngrok (например, `https://abc123.ngrok.io`)

#### Настройка Telegram Webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://abc123.ngrok.io/webhook"
```

Проверка:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

### 9. Интеграция с Tilda

В Zero Block Tilda добавьте код виджета:

```html
<div id="chat-widget"></div>
<script src="https://abc123.ngrok.io/static/chat-widget.js"></script>
```

Убедитесь, что в `main.py` настроен CORS для вашего домена Tilda.

## 📁 Структура проекта

```
artbeauty-bot/
├── main.py              # Flask приложение + Telegram handlers
├── functions.py         # OpenAI, Google Sheets, вспомогательные функции
├── requirements.txt     # Зависимости Python
├── .env                 # Переменные окружения (НЕ коммитится!)
├── .env.example         # Шаблон переменных
├── credentials.json     # Google Service Account (НЕ коммитится!)
├── credentials.json.example  # Шаблон credentials
├── .gitignore           # Исключения для Git
└── README.md            # Документация
```

## 🔧 Основные файлы

### `main.py`
- Flask веб-сервер
- Telegram bot handlers (команды, сообщения)
- Webhook endpoint для Telegram
- API endpoint для веб-виджета (`/widget`)
- Управление сессиями и историей диалогов

### `functions.py`
- Интеграция с OpenAI (GPT + Assistant API)
- Работа с Google Sheets (сохранение заявок)
- Telegram уведомления
- Парсинг и валидация данных записи
- Системные промпты для AI

## 🛠️ Режимы работы

### 1. Telegram Bot
- Обрабатывает команду `/start`
- Консультирует по услугам
- Собирает данные для записи (имя, телефон, услуга, дата, мастер)
- Сохраняет заявку в Google Sheets
- Отправляет уведомление в служебный чат

### 2. Web Widget (Tilda)
- AJAX запросы на `/widget`
- Сохраняет историю диалога в Flask session
- Поддерживает контекст беседы
- Автоматически извлекает данные из сообщений
- Сохраняет заявку при сборе всех полей

## 📊 Google Sheets формат

Таблица должна содержать столбцы:

| Имя | Телефон | Желаемая услуга | Дата и время | Категория мастера | Комментарий |
|-----|---------|-----------------|--------------|-------------------|-------------|
| ... | ...     | ...             | ...          | ...               | ...         |

## 🐛 Отладка

### Проверка webhook Telegram:
```bash
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

### Логи Flask:
```bash
python main.py
```

### Проверка Google Sheets API:
Убедитесь, что Service Account имеет доступ к таблице (права "Редактор")

### Проверка OpenAI Assistant:
Тестируйте промпт в [OpenAI Playground](https://platform.openai.com/playground)

## 🚨 Безопасность

- ✅ Все ключи API в `.env` (не коммитятся в Git)
- ✅ `credentials.json` в `.gitignore`
- ✅ Flask secret key для защиты сессий
- ✅ CORS настроен только для нужных доменов
- ⚠️ При деплое используйте HTTPS
- ⚠️ Не публикуйте `.env` и `credentials.json`

## 📝 Лицензия

Учебный проект. Все ключи API и credentials должны быть заменены на собственные.

## 👨‍💻 Автор

Создано для учебных целей.

## 🤝 Поддержка

При возникновении вопросов:
1. Проверьте все переменные в `.env`
2. Убедитесь, что все API ключи валидны
3. Проверьте доступ Service Account к Google Sheets
4. Убедитесь, что webhook Telegram настроен корректно
