🤖 Универсальный AI-бот для записи клиентов
Telegram-бот и веб-виджет для автоматической записи клиентов с интеграцией OpenAI Assistant, Google Sheets и возможностью подключения к любому сайту.
Подходит для любого бизнеса: салоны красоты, стоматологии, массажные кабинеты, студии йоги, репетиторы, мастерские, фитнес-клубы и многое другое!

🎯 Возможности

✅ Telegram-бот: Автоматические консультации и запись клиентов через Telegram
✅ Веб-виджет: Готовый чат для интеграции на любой сайт (Tilda, WordPress, HTML)
✅ AI-ассистент: OpenAI GPT с собственной базой знаний о вашем бизнесе
✅ Google Sheets: Автоматическое сохранение всех заявок в таблицу
✅ Уведомления: Мгновенные оповещения о новых записях в Telegram-чат
✅ Универсальность: Легко адаптируется под любой тип бизнеса


📋 Требования

Python 3.8 или выше
Telegram Bot Token (бесплатно от @BotFather)
OpenAI API ключ (platform.openai.com)
Google Cloud Service Account для Google Sheets API
Ngrok (для локальной разработки) или VPS/хостинг с HTTPS


📁 Структура проекта
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

🚀 Установка и настройка
Шаг 1: Клонирование и установка зависимостей
bash# Клонируйте репозиторий
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

Шаг 2: Настройка переменных окружения
Создайте файл .env на основе .env.example:
bash# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
Откройте .env и заполните все переменные:
env# === Business Info ===
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

Шаг 3: Создание и настройка Telegram бота
3.1 Создание бота:

Откройте Telegram и найдите @BotFather
Отправьте команду /newbot
Придумайте название (например: "Мой Бот Записи")
Придумайте username (должен заканчиваться на bot, например: my_booking_bot)
Скопируйте полученный токен в .env → TELEGRAM_BOT_TOKEN

3.2 Настройка служебного чата для уведомлений:

Создайте новую группу в Telegram для уведомлений
Добавьте вашего бота в эту группу (через поиск по username)
Отправьте любое тестовое сообщение в группу
Откройте в браузере (замените <YOUR_BOT_TOKEN> на ваш токен):

   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

Найдите в ответе JSON объект с "chat":{"id":-100...}
Скопируйте это отрицательное число в .env → GOOGLE_SERVICE_CHAT_ID

Пример ответа:
json{
  "chat": {
    "id": -1001234567890,  ← Вот это число копируйте
    "title": "Уведомления о записях",
    "type": "group"
  }
}

Шаг 4: Настройка Google Sheets API
4.1 Создание Google Cloud проекта и Service Account:

Перейдите в Google Cloud Console
Создайте новый проект (или выберите существующий)
Включите Google Sheets API:

Меню → APIs & Services → Library
Найдите "Google Sheets API"
Нажмите Enable


Создайте Service Account:

APIs & Services → Credentials
Create Credentials → Service Account
Заполните:

Service account name: booking-bot
Service account ID: (автоматически)


Нажмите Create and Continue
Пропустите опциональные шаги → Done


Создайте JSON ключ:

Найдите созданный Service Account в списке
Нажмите на него
Вкладка Keys → Add Key → Create New Key
Выберите тип JSON
Нажмите Create
Файл credentials.json автоматически скачается


Переместите скачанный credentials.json в корень проекта (рядом с main.py)

4.2 Настройка доступа к Google Таблице:

Создайте новую Google Таблицу или откройте существующую
В первой строке добавьте заголовки столбцов:
ИмяТелефонЖелаемая услугаДата и времяКатегория мастераКомментарий

Нажмите кнопку "Настройки доступа" (Share) в правом верхнем углу
Откройте файл credentials.json и найдите поле client_email (выглядит как: xxx@xxx.iam.gserviceaccount.com)
Скопируйте этот email и добавьте в доступ к таблице
Дайте права "Редактор"
Скопируйте ID таблицы из URL:

   https://docs.google.com/spreadsheets/d/[ВОТ_ЭТОТ_ДЛИННЫЙ_ID]/edit

Вставьте ID в .env → GOOGLE_SHEETS_ID


Шаг 5: Настройка OpenAI
5.1 Получение API ключа:

Перейдите на OpenAI Platform
Зарегистрируйтесь или войдите в аккаунт
Перейдите в раздел API Keys (прямая ссылка)
Нажмите Create new secret key
Скопируйте ключ (он начинается с sk-proj- или sk-)
Вставьте в .env → OPENAI_API_KEY

⚠️ Важно: Ключ показывается только один раз! Сохраните его сразу.
5.2 Создание OpenAI Assistant:

Откройте раздел Assistants
Нажмите Create → New Assistant
Заполните поля:

Name: Booking Assistant (или любое другое название)
Model: Выберите gpt-4-turbo-preview или gpt-3.5-turbo
Instructions: Откройте файл functions.py в проекте, найдите переменную PROMPT и скопируйте весь текст оттуда


Нажмите Save
Скопируйте Assistant ID (начинается с asst_)
Вставьте в .env → OPENAI_ASSISTANT_TOKEN

5.3 Создание базы знаний (2 варианта):
Вариант A: Vector Store (рекомендуется для большой базы знаний)

В разделе Storage → Create Vector Store
Дайте название (например: "Knowledge Base")
Загрузите файл с вашими вопросами-ответами (можно .txt, .json, .docx)
После создания скопируйте Vector Store ID (начинается с vs_)
Вставьте в .env → OPENAI_VECTOR_STORE_ID
Вернитесь к настройкам Assistant → вкладка Tools → включите File Search → выберите ваш Vector Store

Вариант B: Локальный файл (проще для начала)

Создайте файл knowledge_base.json на основе knowledge_base.json.example
Заполните своими вопросами-ответами:

json[
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

Шаг 6: Запуск проекта через Ngrok
Ngrok создаст HTTPS туннель для локального сервера, что необходимо для работы Telegram webhook.
6.1 Установка Ngrok:

Скачайте с ngrok.com/download
Распакуйте в удобную папку
Зарегистрируйтесь на сайте и получите authtoken
Выполните команду (замените на ваш токен):

bash   ngrok config add-authtoken YOUR_AUTH_TOKEN
6.2 Запуск приложения:
Откройте два терминала (или два окна командной строки):
Терминал 1 - Flask приложение:
bashcd booking-assistant-bot
venv\Scripts\activate  # или source venv/bin/activate
python main.py
Вы должны увидеть:
* Running on http://0.0.0.0:5000
Терминал 2 - Ngrok туннель:
bashngrok http 5000
Вы увидите что-то вроде:
Forwarding    https://abc123xyz.ngrok-free.app -> http://localhost:5000
Скопируйте HTTPS URL (например: https://abc123xyz.ngrok-free.app)
6.3 Установка Telegram Webhook:
Откройте браузер или терминал и выполните (замените на ваши данные):
bashcurl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://abc123xyz.ngrok-free.app/webhook"
Пример:
bashcurl -X POST "https://api.telegram.org/bot123456789:ABCdef/setWebhook?url=https://abc123xyz.ngrok-free.app/webhook"
Проверка webhook:
bashcurl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
Должны увидеть:
json{
  "ok": true,
  "result": {
    "url": "https://abc123xyz.ngrok-free.app/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}

Шаг 7: Интеграция веб-виджета на сайт
7.1 Настройка виджета:

Откройте файл chat_widget.html
Найдите строку (примерно строка 123):

javascript   const BACKEND_URL = 'https://YOUR-BACKEND-URL.ngrok-free.app/widget';

Замените на ваш Ngrok URL:

javascript   const BACKEND_URL = 'https://abc123xyz.ngrok-free.app/widget';
7.2 Установка на Tilda:

Откройте страницу в редакторе Tilda
Добавьте блок T123 (HTML-код) или используйте Zero Block
Вставьте весь код из файла chat_widget.html
Сохраните и опубликуйте страницу
Проверьте - в правом нижнем углу должна появиться кнопка чата 💬

7.3 Установка на WordPress:

Установите плагин "Insert Headers and Footers" или "WPCode"
Перейдите в настройки плагина
Вставьте код из chat_widget.html в секцию Footer
Сохраните изменения

7.4 Установка на обычный HTML сайт:
Откройте ваш HTML файл и вставьте код из chat_widget.html перед закрывающим тегом </body>:
html<!DOCTYPE html>
<html>
<head>
    <title>Моя компания</title>
</head>
<body>
    <!-- Контент вашего сайта -->
    
    <!-- Вставьте сюда код из chat_widget.html -->
    
</body>
</html>
7.5 Кастомизация внешнего вида:
В файле chat_widget.html найдите и измените цвета (строки 8, 10, 32, 77, 85):
css/* Основной цвет кнопки и хедера */
background: #6366f1;  /* Измените на свой цвет */

/* Примеры красивых цветов:
   Розовый: #eab1d8
   Синий: #3b82f6
   Зеленый: #10b981
   Фиолетовый: #8b5cf6
   Красный: #ef4444
   Оранжевый: #f97316
*/
Для изменения названия в заголовке чата найдите (строка 95):
html<div id="booking-chat-header">
  Чат с ассистентом  <!-- Измените здесь -->

⚙️ Как это работает
Архитектура:
Клиент (Telegram/Web)
        ↓
Flask Backend (main.py)
        ↓
OpenAI Assistant (functions.py)
        ↓
Google Sheets + Telegram уведомления
Процесс записи через Telegram:

Клиент пишет боту в Telegram
Сообщение обрабатывается через webhook → main.py
OpenAI GPT анализирует намерение и контекст
Если клиент хочет записаться → бот начинает сбор данных:

Имя
Телефон
Услуга
Дата и время
Категория специалиста
Комментарии


После сбора всех данных → автоматическое сохранение в Google Sheets
Уведомление о новой записи отправляется в служебный Telegram-чат

Процесс записи через веб-виджет:

Клиент открывает чат на сайте
Сообщения отправляются на endpoint /widget (POST запрос)
История диалога сохраняется в Flask session (до 10 последних сообщений)
OpenAI обрабатывает запрос с учетом контекста разговора
При сборе всех данных → сохранение в Google Sheets
Уведомление в Telegram-чат


🛠️ Адаптация под свой бизнес
1. Измените информацию в .env:
env# Пример для стоматологии
BUSINESS_NAME=Клиника "Белая Улыбка"
BUSINESS_TYPE=стоматологическая клиника

# Пример для фитнес-студии
BUSINESS_NAME=FitLife Studio
BUSINESS_TYPE=фитнес-центр

# Пример для репетитора
BUSINESS_NAME=Репетиторский центр "Знание"
BUSINESS_TYPE=образовательный центр
2. Создайте базу знаний:
Заполните knowledge_base.json информацией о вашем бизнесе:

📋 Список всех услуг и их описание
💰 Цены на услуги
⏰ График работы (часы, выходные дни)
📍 Адрес, как добраться, парковка
📞 Контакты (телефон, email, соцсети)
❓ Часто задаваемые вопросы (FAQ)
💳 Способы оплаты
🎁 Акции и специальные предложения
👥 Информация о специалистах/мастерах
ℹ️ Политика отмены/переноса записей

3. Настройте структуру Google Sheets под свои нужды:
По умолчанию используется структура:
Имя | Телефон | Желаемая услуга | Дата и время | Категория мастера | Комментарий
Если нужно изменить, отредактируйте в functions.py:
python# Строка 30
SHEET_RANGE = 'A:F'  # Измените диапазон если нужно больше столбцов

# Строка 146-153
def save_application_to_sheets(data: dict):
    values = [[
        data.get('Имя', ''),
        data.get('Телефон', ''),
        # Добавьте свои поля здесь
    ]]

🐛 Решение проблем
❌ Ошибка: "Telegram webhook failed"
Причины:

Ngrok не запущен или URL изменился
Webhook установлен на старый URL

Решение:
bash# 1. Проверьте текущий webhook
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# 2. Удалите старый webhook
curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"

# 3. Установите новый
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://NEW-URL.ngrok-free.app/webhook"
❌ Ошибка: "Google Sheets access denied"
Причины:

credentials.json не найден или неверный
Service Account email не добавлен в таблицу
Google Sheets API не включен

Решение:

Убедитесь, что credentials.json находится в корне проекта
Проверьте, что Service Account email добавлен в вашу таблицу с правами "Редактор"
Проверьте, что Google Sheets API включен в Google Cloud Console

❌ Ошибка: "OpenAI API rate limit exceeded"
Причины:

Превышен лимит запросов
Недостаточно средств на балансе
Неверный API ключ

Решение:

Проверьте баланс: platform.openai.com/account/billing
Проверьте лимиты: platform.openai.com/account/limits
Убедитесь, что API ключ активен и правильно скопирован в .env

❌ Бот не отвечает в Telegram
Чек-лист:

✅ Flask приложение запущено (проверьте терминал)
✅ Ngrok туннель активен (проверьте второй терминал)
✅ Webhook установлен на правильный URL
✅ В .env указан правильный TELEGRAM_BOT_TOKEN
✅ Посмотрите логи в терминале Flask для ошибок

❌ Веб-виджет не работает
Чек-лист:

✅ В chat_widget.html указан правильный BACKEND_URL
✅ Flask приложение запущено
✅ CORS настроен правильно (в main.py)
✅ Откройте консоль браузера (F12) и проверьте ошибки


🚨 Безопасность
✅ Что нужно делать:

Храните все секретные ключи только в .env
Убедитесь, что .env и credentials.json в .gitignore
Используйте сложный случайный FLASK_SECRET_KEY
При деплое на сервер обязательно используйте HTTPS
Регулярно обновляйте зависимости: pip install --upgrade -r requirements.txt
Ограничьте доступ к Google Sheets (давайте права только Service Account)

❌ Чего НЕ нужно делать:

НИКОГДА не публикуйте .env на GitHub
НИКОГДА не коммитьте credentials.json в репозиторий
Не делитесь API ключами в чатах или на форумах
Не используйте HTTP в продакшене (только HTTPS!)
Не храните ключи в коде (только через переменные окружения)


📦 Деплой на продакшн сервер
Вариант 1: VPS (Ubuntu/Debian)
bash# 1. Подключитесь к серверу по SSH
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

# 10. Настройте Nginx как reverse proxy
# 11. Настройте systemd для автозапуска
# 12. Получите SSL сертификат через Let's Encrypt
Вариант 2: Heroku
bash# 1. Установите Heroku CLI
# 2. Создайте Procfile в корне проекта:
echo "web: gunicorn main:app" > Procfile

# 3. Добавьте gunicorn в requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# 4. Инициализируйте git (если еще не сделали)
git init
git add .
git commit -m "Initial commit"

# 5. Создайте приложение на Heroku
heroku create your-app-name

# 6. Добавьте переменные окружения через Heroku Dashboard
# Settings → Config Vars → добавьте все из .env

# 7. Загрузите credentials.json как Config Var
# Преобразуйте в base64 и создайте переменную GOOGLE_CREDENTIALS

# 8. Deploy
git push heroku main

# 9. Установите webhook на Heroku URL
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-app-name.herokuapp.com/webhook"
Вариант 3: Docker (опционально)
Создайте Dockerfile:
dockerfileFROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]

📊 Roadmap (планы развития)

 Интеграция с Google Calendar (автоматическое добавление в календарь)
 Поддержка нескольких языков (мультиязычность)
 Админ-панель для управления записями через веб-интерфейс
 Автоматические SMS/Email напоминания клиентам за день до записи
 Интеграция с платежными системами (онлайн оплата)
 Система подтверждения записей администратором
 Статистика и аналитика (дашборд с графиками)
 WhatsApp бот (в дополнение к Telegram)
 Мобильное приложение для администраторов


📄 Лицензия
MIT License - проект распространяется свободно для личного и коммерческого использования.
⚠️ Важно: Этот проект является учебным. Обязательно замените все API ключи и credentials на собственные перед использованием!

🤝 Поддержка и контрибьюции

Если возникли вопросы:

1. ✅ Проверьте все переменные в `.env`
2. ✅ Убедитесь, что все API ключи валидны
3. ✅ Проверьте доступ к Google Sheets
4. ✅ Убедитесь, что webhook настроен корректно
5. 📝 Откройте Issue на GitHub

Нашли баг или есть предложения?

🐛 Откройте Issue
💡 Предложите улучшение через Pull Request
⭐ Поставьте звезду проекту, если он вам помог!

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
