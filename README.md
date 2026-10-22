# GameDealPulse 🎮

> **GameDealPulse** — сучасна платформа для пошуку знижок на відеоігри, моніторингу цін у 30+ магазинах (Steam, Epic Games, GOG, Humble Bundle, Fanatical тощо) та автоматичного сповіщення про падіння ціни на пошту.

Інтерфейс виконано у темному монохромному кіберпанк-стилі з інтерактивним арт-компонентом **Originkit «Two Reaching Hands»** та реактивним розмиттям під час пошуку.

---

## ⚡ Основні можливості

- **🔍 Пошук знижок у реальному часі**: агрегація пропозицій через CheapShark API з відмовостійкими обкладинками та підтримкою Steam CDN.
- **⭐ Персональний Wishlist**: збереження улюблених ігор та встановлення бажаної ціни купівлі (*Target Price*).
- **📧 Автоматичні Email-сповіщення**: інтеграція з [Resend](https://resend.com) для надсилання листів при зниженні ціни нижче встановленого порогу.
- **🛡️ Вбудований режим емуляції (Mock Email Mode)**: якщо ключ Resend не вказано, додаток не падає, а емулює надсилання листів у консоль — проект працює одразу після клонування!
- **📊 Аналітика цін**: розрахунок відсотка економії, порівняння цін між магазинами та перегляд найнижчої історичної ціни гри.
- **🔐 Безпечна автентифікація**: реєстрація та вхід користувачів з хешуванням паролів (bcrypt) та JWT-токенами.

---

## 🛠️ Стек технологій

- **Backend**: Python 3.10+, [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), SQLite, [HTTPX](https://www.python-httpx.org/), [Pydantic](https://docs.pydantic.dev/).
- **Frontend**: [React 19](https://react.dev/), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/), [Lucide React](https://lucide.dev/), Canvas API.
- **Зовнішні сервіси**:
  - [CheapShark API](https://apidocs.cheapshark.com/) (публічний API знижок, безкоштовний, без реєстрації).
  - [Resend API](https://resend.com/) (відправка транзакційних email).

---

## 🚀 Швидкий запуск проекту

### 1. Клонування репозиторію

```bash
git clone https://github.com/Alavars/gamedeal.git
cd gamedeal
```

### 2. Налаштування віртуального оточення Python

```bash
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# Встановлення залежностей:
pip install -r requirements.txt
```

### 3. Налаштування змінних оточення (`.env`)

Скопіюйте приклад конфігураційного файлу:

```bash
# Windows:
copy .env.example .env
# Linux / macOS:
cp .env.example .env
```

Відкрийте створений файл `.env` у редакторі:
```env
APP_NAME=GameDealPulse
APP_ENV=development
APP_PORT=8000
SECRET_KEY=any_random_secure_string_for_jwt

DATABASE_URL=sqlite:///./data/app.db
CHEAPSHARK_BASE_URL=https://www.cheapshark.com/api/1.0

# Email сервіс (Опціонально):
RESEND_API_KEY=your_resend_api_key_here
SENDER_EMAIL=onboarding@resend.dev
```

> [!NOTE]
> **Чи потрібен власний API ключ?**
> - **CheapShark API**: ключ не потрібен взагалі (публічний відкритий API).
> - **Resend API**: якщо ви хочете отримувати реальні листи на вашу пошту, безкоштовно зареєструйтесь на [resend.com](https://resend.com) та вставте ключ `re_...`.
> - **Якщо у вас немає ключа**: залиште значення за замовчуванням. Програма автоматично перейде у **Mock Mode** і виводитиме сповіщення в консоль сервера. Жодна функція не буде заблокована!

---

### 4. Встановлення та збірка фронтенду

```bash
cd frontend
npm install
npm run build
cd ..
```

---

### 5. Запуск додатка

Запустіть бекенд-сервер, який автоматично роздає скомпільований React-фронтенд:

```bash
python -m uvicorn src.main:app --reload --port 8000
```

Відкрийте у браузері: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

### 💡 Режим розробки фронтенду (опціонально)

Для активної розробки фронтенду з гарячим перезавантаженням (HMR):
```bash
cd frontend
npm run dev
```
Фронтенд буде доступний за адресою: **[http://localhost:5173](http://localhost:5173)**.

---

## 📁 Структура проекту

```text
gamedeal/
├── src/
│   ├── database/       # Моделі SQLAlchemy (User, Game, WishlistItem) та з'єднання
│   ├── routes/         # Ендпоінти FastAPI (auth, deals, wishlist)
│   ├── schemas/        # Pydantic моделі валідації
│   ├── services/       # CheapShark клієнт, Resend мейлер, планувальник перевірки цін
│   ├── utils/          # Хешування паролів та JWT токени
│   ├── config.py       # Pydantic Settings конфігурація
│   └── main.py         # Точка входу FastAPI додатку
├── frontend/           # React + Vite + Tailwind CSS SPA додаток
│   ├── src/
│   │   ├── components/ # React-компоненти (GameCard, GameModal, Wishlist, Artwork)
│   │   ├── api.js      # REST API клієнт для бекенду
│   │   └── App.jsx     # Головний компонент додатку
├── data/               # Локальна SQLite база даних (ігнорується git)
├── .env.example        # Зразок конфігураційного файлу
├── .gitignore          # Налаштування ігнорування секретів і тимчасових файлів
├── requirements.txt    # Залежності Python
└── README.md           # Документація проекту
```

---

## 🧪 Запуск тестів

Для запуску автоматизованих тестів API:
```bash
python tests/test_api_endpoints.py
```
