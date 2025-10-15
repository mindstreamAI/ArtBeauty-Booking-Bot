# 🤖 Универсальный AI-бот для записи клиентов

Telegram-бот и веб-виджет для автоматической записи клиентов с интеграцией OpenAI Assistant, Google Sheets и возможностью подключения к любому сайту (Tilda, WordPress и др.).

**Подходит для любого бизнеса:** салоны красоты, стоматологии, массажные кабинеты, студии йоги, репетиторы, мастерские, фитнес-клубы и многое другое!

---

## 🎯 Возможности

- ✅ **Telegram-бот**: Автоматические консультации и запись клиентов через Telegram
- ✅ **Веб-виджет**: Готовый чат для интеграции на любой сайт (Tilda, WordPress, HTML)
- ✅ **AI-ассистент**: OpenAI GPT с собственной базой знаний о вашем бизнесе
- ✅ **Google Sheets**: Автоматическое сохранение всех заявок в таблицу
- ✅ **Уведомления**: Мгновенные оповещения о новых записях в Telegram-чат
- ✅ **Универсальность**: Легко адаптируется под любой тип бизнеса

---

## 📸 Скриншоты

### Telegram бот - диалог с клиентом
![Telegram бот - консультация](https://github.com/user-attachments/assets/049aa5a0-3315-4ef6-94a0-c5eba8039398)

### Telegram бот - процесс записи
![Telegram бот - запись](https://github.com/user-attachments/assets/19db076d-70a0-48f6-810d-9fec482d4c65)

### Веб-виджет на сайте
![Веб-виджет](https://github.com/user-attachments/assets/885abe99-c8a3-428f-947c-2271a5390988)

### Уведомления в Telegram
![Уведомление о новой записи](https://github.com/user-attachments/assets/88deb98b-64ed-4344-8e7e-d0bafc23cc89)

### Google Sheets - автоматическое сохранение
![Google Sheets](https://github.com/user-attachments/assets/e4d89097-f1dc-4973-9cf2-a4d9daeb766a)

---

## 📋 Требования

- Python 3.8 или выше
- Telegram Bot Token (бесплатно от [@BotFather](https://t.me/botfather))
- OpenAI API ключ ([platform.openai.com](https://platform.openai.com))
- Google Cloud Service Account для Google Sheets API
- Ngrok (для локальной разработки) или VPS/хостинг с HTTPS

---

## 📁 Структура проекта

```
booking-assistant-bot/
├── main.py                      # Flask приложение + Telegram handlers
├── functions.py                 # OpenAI интеграция, Google Sheets, вспомогательные функции
├── requirements.txt             # Python зависимости
├── chat_widget.html             # Готовый веб-виджет для сайта
├── .env                         # Переменные окружения (НЕ коммитится!)
├── .env.example                 # Шаблон с примерами переменных
├── credentials.json             # Google Service Account ключ (НЕ коммитится!)
├── credentials.json.example     # Шаблон credentials.json
├── knowledge_base.json          # База знаний о вашем бизнесе (НЕ коммитится!)
├── knowledge_base.json.example  # Шаблон базы знаний
├── .gitignore                   # Список исключений для Git
└── README.md                    # Эта документация
```

---

## 🚀 Быстрый старт

### 1. Клонирование и установка зависимостей

```bash
# Клонируйте репозиторий
git clone https://github.com/your-username/booking-assistant-bot.git
cd booking-assistant-bot

# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

---

### 2. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Откройте `.env` и заполните все переменные:

```env
# === Business Info ===
BUSINESS_NAME=Ваша Компания
BUSINESS_TYPE=тип бизнеса (например: салон красоты)

# === Flask ===
FLASK_SECRET_KEY=ваш_случайный_секретный_ключ_12345

# === Telegram Bot ===
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# === OpenAI ===
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
OPENAI_ASSISTANT_TOKEN=asst_xxxxxxxxxxxxx
OPENAI_VECTOR_STORE_ID=vs_xxxxxxxxxxxxx

# === Google Sheets ===
GOOGLE_SHEETS_ID=1ABC123XYZ456

# === Service Chat (Telegram) ===
GOOGLE_SERVICE_CHAT_ID=-1001234567890
```

---

### 3. Создание и настройка Telegram бота

#### 3.1 Создание бота:

1. Откройте Telegram и найдите [@BotFather](https://t.me/botfather)
2. Отправьте команду `/newbot`
3. Придумайте название (например: "Мой Бот Записи")
4. Придумайте username (должен заканчиваться на `bot`, например: `my_booking_bot`)
5. Скопируйте полученный токен в `.env` → `TELEGRAM_BOT_TOKEN`

#### 3.2 Настройка служебного чата для уведомлений:

1. Создайте новую группу в Telegram для уведомлений
2. Добавьте вашего бота в эту группу (через поиск по username)
3. Отправьте любое тестовое сообщение в группу
4. Откройте в браузере (замените `<YOUR_BOT_TOKEN>` на ваш токен):
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
5. Найдите в ответе JSON объект с `"chat":{"id":-100...}`
6. Скопируйте это отрицательное число в `.env` → `GOOGLE_SERVICE_CHAT_ID`

---

### 4. Настройка Google Sheets API

#### 4.1 Создание Google Cloud проекта и Service Account:

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект (или выберите существующий)
3. Включите Google Sheets API:
   - Меню → **APIs & Services** → **Library**
   - Найдите "Google Sheets API"
   - Нажмите **Enable**

4. Создайте Service Account:
   - **APIs & Services** → **Credentials**
   - **Create Credentials** → **Service Account**
   - Заполните:
     - **Service account name**: booking-bot
     - **Service account ID**: (автоматически)
   - Нажмите **Create and Continue**
   - Пропустите опциональные шаги → **Done**

5. Создайте JSON ключ:
   - Найдите созданный Service Account в списке
   - Нажмите на него
   - Вкладка **Keys** → **Add Key** → **Create New Key**
   - Выберите тип **JSON**
   - Нажмите **Create**
   - Файл `credentials.json` автоматически скачается

6. Переместите скачанный `credentials.json` в корень проекта (рядом с `main.py`)

#### 4.2 Настройка доступа к Google Таблице:

1. Создайте новую Google Таблицу или откройте существующую
2. В первой строке добавьте заголовки столбцов:

   | Имя | Телефон | Желаемая услуга | Дата и время | Категория мастера | Комментарий |
   |-----|---------|-----------------|--------------|-------------------|-------------|

3. Нажмите кнопку **"Настройки доступа"** (Share) в правом верхнем углу
4. Откройте файл `credentials.json` и найдите поле `client_email` (выглядит как: `xxx@xxx.iam.gserviceaccount.com`)
5. Скопируйте этот email и добавьте в доступ к таблице
6. Дайте права **"Редактор"**
7. Скопируйте ID таблицы из URL:
   ```
   https://docs.google.com/spreadsheets/d/[ВОТ_ЭТОТ_ДЛИННЫЙ_ID]/edit
   ```
8. Вставьте ID в `.env` → `GOOGLE_SHEETS_ID`

---

### 5. Настройка OpenAI

#### 5.1 Получение API ключа:

1. Перейдите на [OpenAI Platform](https://platform.openai.com/)
2. Зарегистрируйтесь или войдите в аккаунт
3. Перейдите в раздел **API Keys** ([прямая ссылка](https://platform.openai.com/api-keys))
4. Нажмите **Create new secret key**
5. Скопируйте ключ (он начинается с `sk-proj-` или `sk-`)
6. Вставьте в `.env` → `OPENAI_API_KEY`

**⚠️ Важно:** Ключ показывается только один раз! Сохраните его сразу.

#### 5.2 Создание OpenAI Assistant:

1. Откройте раздел [Assistants](https://platform.openai.com/assistants)
2. Нажмите **Create** → **New Assistant**
3. Заполните поля:
   - **Name**: Booking Assistant (или любое другое название)
   - **Model**: Выберите `gpt-4-turbo-preview` или `gpt-3.5-turbo`
   - **Instructions**: Откройте файл `functions.py` в проекте, найдите переменную `PROMPT` и скопируйте весь текст оттуда
4. Нажмите **Save**
5. Скопируйте **Assistant ID** (начинается с `asst_`)
6. Вставьте в `.env` → `OPENAI_ASSISTANT_TOKEN`

#### 5.3 Создание базы знаний:

**Вариант A: Vector Store (рекомендуется)**

1. В разделе [Storage](https://platform.openai.com/storage) → **Create Vector Store**
2. Дайте название (например: "Knowledge Base")
3. Загрузите файл с вашими вопросами-ответами (можно `.txt`, `.json`, `.docx`)
4. После создания скопируйте **Vector Store ID** (начинается с `vs_`)
5. Вставьте в `.env` → `OPENAI_VECTOR_STORE_ID`
6. Вернитесь к настройкам Assistant → вкладка **Tools** → включите **File Search** → выберите ваш Vector Store

**Вариант B: Локальный файл**

Создайте `knowledge_base.json` на основе `knowledge_base.json.example`:

```json
[
  {
    "Вопросы": "Какие у вас часы работы?",
    "Ответы": "Мы работаем пн-сб с 10:00 до 20:00, воскресенье - выходной"
  },
  {
    "Вопросы": "Какой у вас адрес?",
    "Ответы": "г. Москва, ул. Примерная, д. 1, офис 10"
  },
  {
    "Вопросы": "Как можно оплатить услуги?",
    "Ответы": "Мы принимаем наличные, банковские карты и электронные платежи"
  }
]
```

---

### 6. Запуск проекта через Ngrok

Ngrok создаст HTTPS туннель для локального сервера, что необходимо для работы Telegram webhook.

#### 6.1 Установка Ngrok:

1. Скачайте с [ngrok.com/download](https://ngrok.com/download)
2. Распакуйте в удобную папку
3. Зарегистрируйтесь на сайте и получите **authtoken**
4. Выполните команду (замените на ваш токен):
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

#### 6.2 Запуск приложения:

Откройте **два терминала** (или два окна командной строки):

**Терминал 1** - Flask приложение:
```bash
cd booking-assistant-bot
venv\Scripts\activate  # или source venv/bin/activate
python main.py
```

Вы должны увидеть:
```
* Running on http://0.0.0.0:5000
```

**Терминал 2** - Ngrok туннель:
```bash
ngrok http 5000
```

Вы увидите что-то вроде:
```
Forwarding    https://abc123xyz.ngrok-free.app -> http://localhost:5000
```

**Скопируйте HTTPS URL** (например: `https://abc123xyz.ngrok-free.app`)

#### 6.3 Установка Telegram Webhook:

Откройте браузер или терминал и выполните (замените на ваши данные):

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://abc123xyz.ngrok-free.app/webhook"
```

**Проверка webhook:**
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

Должны увидеть:
```json
{
  "ok": true,
  "result": {
    "url": "https://abc123xyz.ngrok-free.app/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

---

### 7. Интеграция веб-виджета на сайт

#### 7.1 Настройка виджета:

1. Откройте файл `chat_widget.html`
2. Найдите строку (примерно строка 123):
   ```javascript
   const BACKEND_URL = 'https://YOUR-BACKEND-URL.ngrok-free.app/widget';
   ```
3. Замените на ваш Ngrok URL:
   ```javascript
   const BACKEND_URL = 'https://abc123xyz.ngrok-free.app/widget';
   ```

#### 7.2 Установка на Tilda:

1. Откройте страницу в редакторе Tilda
2. Добавьте блок **T123** (HTML-код) или используйте **Zero Block**
3. Вставьте **весь код** из файла `chat_widget.html`
4. Сохраните и опубликуйте страницу
5. Проверьте - в правом нижнем углу должна появиться кнопка чата 💬

#### 7.3 Установка на WordPress:

1. Установите плагин **"Insert Headers and Footers"** или **"WPCode"**
2. Перейдите в настройки плагина
3. Вставьте код из `chat_widget.html` в секцию **Footer**
4. Сохраните изменения

#### 7.4 Установка на обычный HTML сайт:

Откройте ваш HTML файл и вставьте код из `chat_widget.html` перед закрывающим тегом `</body>`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Моя компания</title>
</head>
<body>
    <!-- Контент вашего сайта -->
    
    <!-- Вставьте сюда код из chat_widget.html -->
    
</body>
</html>
```

#### 7.5 Кастомизация внешнего вида:

В файле `chat_widget.html` найдите и измените цвета (строки 8, 10, 32, 77, 85):

```css
/* Основной цвет кнопки и хедера */
background: #6366f1;  /* Измените на свой цвет */

/* Примеры красивых цветов:
   Розовый: #eab1d8
   Синий: #3b82f6
   Зеленый: #10b981
   Фиолетовый: #8b5cf6
   Красный: #ef4444
   Оранжевый: #f97316
*/
```

---

## ⚙️ Как это работает

### Архитектура:

```
Клиент (Telegram/Web)
        ↓
Flask Backend (main.py)
        ↓
OpenAI Assistant (functions.py)
        ↓
Google Sheets + Telegram уведомления
```

### Процесс записи через Telegram:

1. Клиент пишет боту в Telegram
2. Сообщение обрабатывается через webhook → `main.py`
3. OpenAI GPT анализирует намерение и контекст
4. Если клиент хочет записаться → бот начинает сбор данных
5. После сбора всех данных → автоматическое сохранение в Google Sheets
6. Уведомление о новой записи отправляется в служебный Telegram-чат

### Процесс записи через веб-виджет:

1. Клиент открывает чат на сайте
2. Сообщения отправляются на endpoint `/widget` (POST запрос)
3. История диалога сохраняется в Flask session
4. OpenAI обрабатывает запрос с учетом контекста разговора
5. При сборе всех данных → сохранение в Google Sheets
6. Уведомление в Telegram-чат

---

## 🛠️ Адаптация под свой бизнес

### 1. Измените информацию в `.env`:

```env
# Пример для стоматологии
BUSINESS_NAME=Клиника "Белая Улыбка"
BUSINESS_TYPE=стоматологическая клиника

# Пример для фитнес-студии
BUSINESS_NAME=FitLife Studio
BUSINESS_TYPE=фитнес-центр

# Пример для репетитора
BUSINESS_NAME=Репетиторский центр "Знание"
BUSINESS_TYPE=образовательный центр
```

### 2. Создайте базу знаний:

Заполните `knowledge_base.json` информацией о вашем бизнесе:

- 📋 Список всех услуг и их описание
- 💰 Цены на услуги
- ⏰ График работы (часы, выходные дни)
- 📍 Адрес, как добраться, парковка
- 📞 Контакты (телефон, email, соцсети)
- ❓ Часто задаваемые вопросы (FAQ)
- 💳 Способы оплаты
- 🎁 Акции и специальные предложения
- 👥 Информация о специалистах/мастерах
- ℹ️ Политика отмены/переноса записей

### 3. Настройте структуру Google Sheets под свои нужды:

По умолчанию используется структура:
```
Имя | Телефон | Желаемая услуга | Дата и время | Категория мастера | Комментарий
```

Если нужно изменить, отредактируйте в `functions.py`:
```python
# Строка 30
SHEET_RANGE = 'A:F'  # Измените диапазон если нужно больше столбцов

# Строка 146-153
def save_application_to_sheets(data: dict):
    values = [[
        data.get('Имя', ''),
        data.get('Телефон', ''),
        # Добавьте свои поля здесь
    ]]
```

---

## 🐛 Решение проблем

### ❌ Ошибка: "Telegram webhook failed"

**Решение:**
```bash
# 1. Проверьте текущий webhook
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# 2. Удалите старый webhook
curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"

# 3. Установите новый
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://NEW-URL.ngrok-free.app/webhook"
```

### ❌ Ошибка: "Google Sheets access denied"

**Решение:**
1. Убедитесь, что `credentials.json` находится в корне проекта
2. Проверьте, что Service Account email добавлен в вашу таблицу с правами "Редактор"
3. Проверьте, что Google Sheets API включен в Google Cloud Console

### ❌ Ошибка: "OpenAI API rate limit exceeded"

**Решение:**
1. Проверьте баланс: [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
2. Проверьте лимиты: [platform.openai.com/account/limits](https://platform.openai.com/account/limits)
3. Убедитесь, что API ключ активен и правильно скопирован в `.env`

### ❌ Бот не отвечает в Telegram

**Чек-лист:**
- ✅ Flask приложение запущено (проверьте терминал)
- ✅ Ngrok туннель активен (проверьте второй терминал)
- ✅ Webhook установлен на правильный URL
- ✅ В `.env` указан правильный `TELEGRAM_BOT_TOKEN`
- ✅ Посмотрите логи в терминале Flask для ошибок

### ❌ Веб-виджет не работает

**Чек-лист:**
- ✅ В `chat_widget.html` указан правильный `BACKEND_URL`
- ✅ Flask приложение запущено
- ✅ CORS настроен правильно (в `main.py`)
- ✅ Откройте консоль браузера (F12) и проверьте ошибки

---

## 🚨 Безопасность

### ✅ Что нужно делать:

- Храните все секретные ключи только в `.env`
- Убедитесь, что `.env` и `credentials.json` в `.gitignore`
- Используйте сложный случайный `FLASK_SECRET_KEY`
- При деплое на сервер обязательно используйте HTTPS
- Регулярно обновляйте зависимости: `pip install --upgrade -r requirements.txt`
- Ограничьте доступ к Google Sheets (давайте права только Service Account)

### ❌ Чего НЕ нужно делать:

- **НИКОГДА** не публикуйте `.env` на GitHub
- **НИКОГДА** не коммитьте `credentials.json` в репозиторий
- Не делитесь API ключами в чатах или на форумах
- Не используйте HTTP в продакшене (только HTTPS!)
- Не храните ключи в коде (только через переменные окружения)

---

## 📦 Деплой на продакшн сервер

### Вариант 1: VPS (Ubuntu/Debian)

```bash
# 1. Подключитесь к серверу по SSH
ssh user@your-server-ip

# 2. Обновите систему
sudo apt update && sudo apt upgrade -y

# 3. Установите Python и зависимости
sudo apt install python3 python3-pip python3-venv nginx -y

# 4. Клонируйте проект
git clone https://github.com/your-username/booking-assistant-bot.git
cd booking-assistant-bot

# 5. Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 6. Установите зависимости
pip install -r requirements.txt

# 7. Настройте .env и загрузите credentials.json

# 8. Установите Gunicorn для продакшена
pip install gunicorn

# 9. Запустите через Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Вариант 2: Heroku

```bash
# 1. Установите Heroku CLI
# 2. Создайте Procfile в корне проекта:
echo "web: gunicorn main:app" > Procfile

# 3. Добавьте gunicorn в requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# 4. Deploy
heroku create your-app-name
git push heroku main

# 5. Установите webhook на Heroku URL
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-app-name.herokuapp.com/webhook"
```

---

## 📊 Roadmap (планы развития)

- [ ] Интеграция с Google Calendar (автоматическое добавление в календарь)
- [ ] Поддержка нескольких языков (мультиязычность)
- [ ] Админ-панель для управления записями через веб-интерфейс
- [ ] Автоматические SMS/Email напоминания клиентам за день до записи
- [ ] Интеграция с платежными системами (онлайн оплата)
- [ ] Система подтверждения записей администратором
- [ ] Статистика и аналитика (дашборд с графиками)
- [ ] WhatsApp бот (в дополнение к Telegram)

---

## 📄 Лицензия

MIT License - проект распространяется свободно для личного и коммерческого использования.

**⚠️ Важно:** Этот проект является учебным. Обязательно замените все API ключи и credentials на собственные перед использованием!

---

## 🤝 Поддержка и контрибьюции

### Нашли баг или есть предложения?

- 🐛 Откройте [Issue](https://github.com/your-username/booking-assistant-bot/issues)
- 💡 Предложите улучшение через [Pull Request](https://github.com/your-username/booking-assistant-bot/pulls)
- ⭐ Поставьте звезду проекту, если он вам помог!

### Перед обращением за помощью:

1. ✅ Проверьте все переменные в `.env`
2. ✅ Убедитесь, что все API ключи валидны и активны
3. ✅ Проверьте доступ Service Account к Google Sheets
4. ✅ Убедитесь, что webhook Telegram настроен корректно
5. ✅ Посмотрите логи в терминале Flask приложения
6. ✅ Прочитайте раздел "Решение проблем" выше

---

## 🎓 Примеры использования для разных бизнесов

### 💇 Салон красоты

```env
BUSINESS_NAME=Beauty Studio ArtHair
BUSINESS_TYPE=салон красоты
```

**База знаний должна содержать:**
- Услуги: стрижки, окрашивание, укладки, уход
- Категории мастеров и разница в ценах
- Время на каждую процедуру
- Рекомендации по уходу после процедур

---

### 🦷 Стоматология

```env
BUSINESS_NAME=Стоматологическая клиника "Белая Улыбка"
BUSINESS_TYPE=стоматологическая клиника
```

**База знаний должна содержать:**
- Виды услуг: лечение, имплантация, отбеливание
- Врачи и их специализация
- Подготовка к приему
- Страховка и оплата

---

### 🧘 Студия йоги / Фитнес

```env
BUSINESS_NAME=Yoga Life Studio
BUSINESS_TYPE=студия йоги
```

**База знаний должна содержать:**
- Расписание групповых занятий
- Персональные тренировки
- Абонементы и разовые посещения
- Что взять с собой на занятие
- Уровни сложности для новичков

---

### 📚 Репетиторский центр

```env
BUSINESS_NAME=Образовательный центр "Знание"
BUSINESS_TYPE=репетиторский центр
```

**База знаний должна содержать:**
- Предметы и направления
- Формат занятий (онлайн/оффлайн)
- Стоимость академического часа
- Квалификация преподавателей
- Пробный урок

---

### 🔧 Автосервис / Мастерская

```env
BUSINESS_NAME=Автосервис "Мастер"
BUSINESS_TYPE=автосервис
```

**База знаний должна содержать:**
- Виды работ: ТО, ремонт, диагностика
- Марки автомобилей
- Время выполнения работ
- Гарантия на услуги
- Запчасти (оригинал/аналог)

---

## 📈 Статистика и мониторинг

### Просмотр записей в Google Sheets:

1. Откройте вашу таблицу
2. Все новые записи добавляются автоматически
3. Можно добавить столбец "Статус" (подтверждено/отменено)
4. Используйте фильтры и сортировку для удобства

### Мониторинг уведомлений:

- Все новые записи приходят в ваш служебный Telegram-чат
- Настройте звук уведомлений для этого чата
- Можно добавить несколько администраторов в группу

---

## 🔄 Обновление проекта

Когда выйдут обновления или вы захотите внести изменения:

```bash
# Перейдите в папку проекта
cd booking-assistant-bot

# Активируйте виртуальное окружение
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Обновите зависимости (если изменился requirements.txt)
pip install --upgrade -r requirements.txt

# Перезапустите приложение
# Остановите старый процесс (Ctrl+C) и запустите снова:
python main.py
```

---

## 📚 Дополнительные ресурсы

### Документация используемых технологий:

- [Flask документация](https://flask.palletsprojects.com/)
- [python-telegram-bot](https://docs.python-telegram-bot.org/)
- [OpenAI API](https://platform.openai.com/docs)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Ngrok документация](https://ngrok.com/docs)

### Полезные статьи:

- [Как работают Telegram боты](https://core.telegram.org/bots)
- [Best practices для Flask приложений](https://flask.palletsprojects.com/en/stable/patterns/)
- [Промпт инжиниринг для ChatGPT](https://platform.openai.com/docs/guides/prompt-engineering)

---

## ⚡ Быстрый запуск (краткая версия)

Для тех, кто уже знаком с разработкой:

```bash
# 1. Клонируйте и установите
git clone https://github.com/your-username/booking-assistant-bot.git
cd booking-assistant-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Настройте .env (скопируйте .env.example)
cp .env.example .env
# Заполните все переменные в .env

# 3. Добавьте credentials.json от Google

# 4. Создайте knowledge_base.json

# 5. Запустите
python main.py

# 6. В другом терминале запустите ngrok
ngrok http 5000

# 7. Установите webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<NGROK-URL>/webhook"

# 8. Готово! Пишите боту в Telegram
```

---

## 🌟 Особенности и преимущества

### Почему стоит использовать этот бот:

✅ **Полностью автоматизированный** - записывает клиентов без участия администратора  
✅ **Умный AI** - понимает контекст разговора и естественный язык  
✅ **Универсальный** - подходит для любого типа бизнеса  
✅ **Бесплатный** - open source проект без лицензионных отчислений  
✅ **Простая интеграция** - готовый виджет для сайта за 5 минут  
✅ **Google Sheets** - простое управление заявками без сложных CRM  
✅ **Telegram уведомления** - мгновенные оповещения на ваш телефон  
✅ **База знаний** - бот отвечает на вопросы о вашем бизнесе 24/7  

---

## 💡 Советы по использованию

### Для максимальной эффективности:

1. **Подробная база знаний** - чем больше информации, тем лучше бот консультирует
2. **Быстрый ответ** - отвечайте клиентам в течение 1-2 часов после записи
3. **Тестирование** - проверьте бота перед запуском, запишитесь сами
4. **Обратная связь** - спрашивайте клиентов, было ли им удобно
5. **Регулярные обновления** - дополняйте базу знаний новыми вопросами

---

## 🎬 Видео-инструкции (скоро)

- [ ] Полная установка за 15 минут
- [ ] Настройка OpenAI Assistant
- [ ] Интеграция виджета на Tilda
- [ ] Кастомизация под свой бизнес
- [ ] Деплой на сервер

---

## 📞 Контакты

Если у вас есть вопросы по проекту или предложения по сотрудничеству:

- 📧 Email: your-email@example.com
- 💬 Telegram: @your_username
- 🐙 GitHub: [your-username](https://github.com/your-username)

---

## ⭐ Поддержите проект

Если этот проект был вам полезен:

- ⭐ Поставьте звезду на GitHub
- 🔄 Поделитесь с друзьями и коллегами
- 💬 Напишите отзыв или кейс использования
- 🤝 Сделайте Pull Request с улучшениями

---

## 🏆 Авторы и благодарности

**Создатель проекта:** [Ваше имя](https://github.com/your-username)

**Благодарности:**
- OpenAI за мощный API
- Telegram за Bot API
- Сообществу разработчиков за вдохновение

---

## 📝 История изменений

### v1.0.0 (2025)
- ✅ Первый релиз
- ✅ Telegram бот с AI консультантом
- ✅ Веб-виджет для сайтов
- ✅ Интеграция с Google Sheets
- ✅ Система уведомлений
- ✅ База знаний

---

**Удачи в автоматизации вашего бизнеса! 🚀**

---

## 📌 Быстрые ссылки

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenAI Platform](https://platform.openai.com/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Ngrok](https://ngrok.com/)
- [Flask документация](https://flask.palletsprojects.com/)

---
