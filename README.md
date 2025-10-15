# 🤖 Универсальный AI-бот для записи клиентов

Telegram-бот и веб-виджет для автоматической записи клиентов с интеграцией OpenAI Assistant, Google Sheets и возможностью подключения к любому сайту (Tilda, WordPress и др.).

**Подходит для любого бизнеса:** салоны красоты, стоматологии, массажные кабинеты, студии йоги, репетиторы, мастерские и многое другое!

---

## 🎯 Возможности

- ✅ **Telegram-бот**: Автоматические консультации и запись клиентов
- ✅ **Веб-виджет**: Интеграция чата на любой сайт
- ✅ **AI-ассистент**: OpenAI GPT с собственной базой знаний
- ✅ **Google Sheets**: Автоматическое сохранение заявок в таблицу
- ✅ **Уведомления**: Мгновенные оповещения о новых записях в Telegram
- ✅ **Универсальность**: Легко адаптируется под любой бизнес

---

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- OpenAI API ключ
- Google Cloud Service Account (для Google Sheets API)
- Ngrok (для локальной разработки) или сервер с HTTPS

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/booking-assistant-bot.git
cd booking-assistant-bot
```

### 2. Установка зависимостей

Создайте виртуальное окружение:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Установите библиотеки:

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Скопируйте шаблон и заполните данными:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Откройте `.env` и заполните:

```env
# === Business Info ===
BUSINESS_NAME=Ваша Компания
BUSINESS_TYPE=салон красоты

# === Flask ===
FLASK_SECRET_KEY=ваш_случайный_ключ_123456

# === Telegram Bot ===
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl...

# === OpenAI ===
OPENAI_API_KEY=sk-proj-...
OPENAI_ASSISTANT_TOKEN=asst_...

# === Google Sheets ===
GOOGLE_SHEETS_ID=1YL3vdLFKCs8...

# === Service Chat ===
GOOGLE_SERVICE_CHAT_ID=-1002345678901
```

---

## 📝 Подробная настройка

### Шаг 1: Создание Telegram бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot`
3. Придумайте название и username для бота
4. Скопируйте полученный токен в `.env` → `TELEGRAM_BOT_TOKEN`

**Настройка служебного чата для уведомлений:**

1. Создайте группу или канал
2. Добавьте вашего бота в группу
3. Отправьте любое сообщение
4. Получите chat_id:
   ```bash
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
5. Найдите `"chat":{"id":-100...}` и скопируйте в `.env` → `GOOGLE_SERVICE_CHAT_ID`

---

### Шаг 2: Настройка Google Sheets

#### Создание Service Account:

1. Откройте [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте проект или выберите существующий
3. Включите **Google Sheets API**:
   - Navigation Menu → APIs & Services → Library
   - Найдите "Google Sheets API" → Enable
4. Создайте Service Account:
   - APIs & Services → Credentials
   - Create Credentials → Service Account
   - Заполните форму и создайте
5. Создайте ключ:
   - Откройте созданный Service Account
   - Keys → Add Key → Create New Key → JSON
   - Скачается файл `credentials.json`
6. Переместите `credentials.json` в корень проекта

#### Настройка доступа к таблице:

1. Создайте новую Google Таблицу или откройте существующую
2. Добавьте заголовки столбцов:
   
   | Имя | Телефон | Желаемая услуга | Дата и время | Категория мастера | Комментарий |
   |-----|---------|-----------------|--------------|-------------------|-------------|

3. Нажмите "Поделиться" (Share)
4. Добавьте email из `credentials.json` (поле `client_email`)
5. Дайте права **Редактор**
6. Скопируйте ID таблицы из URL:
   ```
   https://docs.google.com/spreadsheets/d/[ВОТ_ЭТОТ_ID]/edit
   ```
7. Вставьте ID в `.env` → `GOOGLE_SHEETS_ID`

---

### Шаг 3: Настройка OpenAI Assistant

#### Создание API ключа:

1. Перейдите на [OpenAI Platform](https://platform.openai.com/)
2. API Keys → Create new secret key
3. Скопируйте ключ в `.env` → `OPENAI_API_KEY`

#### Создание Assistant:

1. Откройте раздел [Assistants](https://platform.openai.com/assistants)
2. Create → New Assistant
3. Настройте:
   - **Name**: Booking Assistant
   - **Model**: gpt-4-turbo или gpt-3.5-turbo
   - **Instructions**: Скопируйте промпт из `functions.py` (переменная `PROMPT`)
4. Скопируйте Assistant ID (начинается с `asst_...`)
5. Вставьте в `.env` → `OPENAI_ASSISTANT_TOKEN`

#### Создание базы знаний (опционально):

**Вариант 1: Vector Store (рекомендуется)**

1. В разделе **Storage** → Create Vector Store
2. Загрузите файл `knowledge_base.json` с вашими вопросами-ответами
3. Привяжите Vector Store к Assistant (в настройках Assistant)
4. ID Vector Store можно добавить в `.env` → `OPENAI_VECTOR_STORE_ID`

**Вариант 2: Файл в проекте**

1. Создайте `knowledge_base.json` на основе `knowledge_base.json.example`
2. Заполните своими вопросами и ответами о бизнесе:

```json
[
  {
    "Вопросы": "Какие у вас часы работы?",
    "Ответы": "Мы работаем пн-сб с 10:00 до 20:00"
  },
  {
    "Вопросы": "Какой у вас адрес?",
    "Ответы": "г. Москва, ул. Примерная, д. 1"
  }
]
```

---

### Шаг 4: Запуск через Ngrok

Ngrok создаст HTTPS туннель для локального тестирования.

#### Установка Ngrok:

1. Скачайте с [ngrok.com/download](https://ngrok.com/download)
2. Зарегистрируйтесь и получите authtoken
3. Настройте:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

#### Запуск:

**Терминал 1** - Flask приложение:
```bash
python main.py
```

**Терминал 2** - Ngrok:
```bash
ngrok http 5000
```

Скопируйте HTTPS URL (например, `https://abc123.ngrok-free.app`)

#### Настройка Telegram Webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://abc123.ngrok-free.app/webhook"
```

Проверка:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

---

### Шаг 5: Интеграция с сайтом (опционально)

#### Для Tilda:

В Zero Block добавьте:

```html
<div id="chat-widget"></div>
<script>
  // Ваш код виджета чата
  // Endpoint: https://abc123.ngrok-free.app/widget
</script>
```

#### Для других платформ:

Используйте endpoint `/widget` для POST запросов с JSON:

```javascript
fetch('https://your-domain.com/widget', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'Привет'})
})
```

---

## 📁 Структура проекта

```
booking-assistant-bot/
├── main.py                      # Flask + Telegram handlers
├── functions.py                 # OpenAI, Google Sheets, логика
├── requirements.txt             # Зависимости
├── .env                         # Переменные окружения (не коммитится!)
├── .env.example                 # Шаблон .env
├── credentials.json             # Google Service Account (не коммитится!)
├── credentials.json.example     # Шаблон credentials
├── knowledge_base.json          # База знаний (не коммитится!)
├── knowledge_base.json.example  # Шаблон базы знаний
├── .gitignore                   # Список игнорируемых файлов
└── README.md                    # Эта документация
```

---

## ⚙️ Как это работает

### Telegram Bot:

1. Клиент пишет боту
2. GPT анализирует сообщение и распознает намерение
3. Если нужна запись → бот собирает данные пошагово
4. Все данные сохраняются в Google Sheets
5. Уведомление приходит в служебный чат

### Web Widget:

1. Клиент пишет в чат на сайте
2. Сообщение отправляется на endpoint `/widget`
3. История диалога сохраняется в Flask session
4. GPT обрабатывает запрос с учетом контекста
5. При сборе всех данных → сохранение в Google Sheets

---

## 🛠️ Адаптация под свой бизнес

### 1. Измените информацию в `.env`:

```env
BUSINESS_NAME=Стоматология "Белый зуб"
BUSINESS_TYPE=стоматологическая клиника
```

### 2. Создайте базу знаний:

Заполните `knowledge_base.json` вопросами о вашем бизнесе:
- Услуги и цены
- Режим работы
- Адрес и контакты
- Часто задаваемые вопросы
- Особенности и преимущества

### 3. Настройте Google Sheets:

Измените столбцы под ваши нужды (в `functions.py` → `SHEET_RANGE`)

### 4. Доработайте промпт (опционально):

В `functions.py` → переменная `PROMPT` - добавьте специфику вашего бизнеса

---

## 🐛 Решение проблем

### Ошибка: "Webhook failed"

```bash
# Проверьте webhook
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Удалите старый webhook
curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"

# Установите новый
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-url.com/webhook"
```

### Ошибка: Google Sheets access denied

- Убедитесь, что `credentials.json` находится в корне проекта
- Проверьте, что Service Account email добавлен в таблицу с правами "Редактор"
- Включена ли Google Sheets API в вашем проекте?

### Ошибка: OpenAI API rate limit

- Проверьте баланс на [platform.openai.com](https://platform.openai.com/account/billing)
- Убедитесь, что API ключ активен

### Бот не отвечает

- Проверьте, что Flask приложение запущено
- Проверьте, что Ngrok туннель активен
- Посмотрите логи в терминале Flask приложения

---

## 🚨 Безопасность

✅ **Что делать:**
- Все секретные ключи в `.env`
- `.env` и `credentials.json` в `.gitignore`
- Используйте сложный `FLASK_SECRET_KEY`
- При деплое используйте HTTPS

❌ **Чего НЕ делать:**
- Не публикуйте `.env` на GitHub
- Не коммитьте `credentials.json`
- Не делитесь API ключами
- Не используйте HTTP в продакшене

---

## 📦 Деплой на сервер

### Вариант 1: VPS (Ubuntu)

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Python и зависимости
sudo apt install python3 python3-pip python3-venv -y

# Клонируйте проект
git clone https://github.com/your-username/booking-assistant-bot.git
cd booking-assistant-bot

# Создайте venv
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Настройте .env и credentials.json

# Используйте systemd или supervisor для автозапуска
# Установите nginx для reverse proxy
```

### Вариант 2: Heroku

```bash
# Установите Heroku CLI
# Создайте Procfile:
web: python main.py

# Добавьте переменные окружения в Heroku Dashboard
# Deploy через Git
```

### Вариант 3: Docker (скоро)

---

## 📄 Лицензия

MIT License - учебный проект для свободного использования.

**Важно:** Замените все API ключи и credentials на собственные!

---

## 🤝 Поддержка

Если возникли вопросы:

1. ✅ Проверьте все переменные в `.env`
2. ✅ Убедитесь, что все API ключи валидны
3. ✅ Проверьте доступ к Google Sheets
4. ✅ Убедитесь, что webhook настроен корректно
5. 📝 Откройте Issue на GitHub

---

## 🎓 Примеры использования

### Салон красоты
```env
BUSINESS_NAME=Beauty Studio
BUSINESS_TYPE=салон красоты
```

### Стоматология
```env
BUSINESS_NAME=Dental Clinic
BUSINESS_TYPE=стоматологическая клиника
```

### Фитнес-студия
```env
BUSINESS_NAME=FitLife
BUSINESS_TYPE=фитнес-студия
```

### Репетиторство
```env
BUSINESS_NAME=Math Tutor
BUSINESS_TYPE=репетиторский центр
```

---

## 📊 Roadmap

- [ ] Интеграция с календарями (Google Calendar)
- [ ] Поддержка множественных языков
- [ ] Админ-панель для управления записями
- [ ] Автоматические напоминания клиентам
- [ ] Интеграция с платежными системами

---

**Удачи в автоматизации вашего бизнеса! 🚀**
