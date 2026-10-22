# GameDealPulse 🎮

> **GameDealPulse** is a modern video game deal aggregator and price tracking platform. It monitors video game discounts across 30+ digital storefronts (Steam, Epic Games Store, GOG, Humble Bundle, Fanatical, etc.) and provides automated email alerts when games reach a user's desired target price.

The user interface features a sleek dark monochrome cyberpunk theme, smooth animations, resilient image fallbacks, and the interactive **Originkit "Two Reaching Hands"** artwork backdrop.

---

## ⚡ Key Features

- **🔍 Real-Time Game Deal Search**: Instant multi-store deal aggregation powered by the CheapShark API with direct store links and Steam CDN artwork support.
- **⭐ Personalized Wishlist**: Save favorite games and set custom purchase price targets (*Target Price Alert*).
- **📧 Automated Price Drop Notifications**: Integrated with [Resend](https://resend.com) to automatically dispatch email notifications when deals drop below your target price.
- **🛡️ Built-in Mock Email Mode**: If no Resend API key is provided, the application runs in a safe **Mock Mode** (logging alerts directly to the console) — the project works immediately after cloning without requiring third-party registration!
- **📊 Deal Analytics & Statistics**: Calculates discount percentages, compares pricing across stores, and displays the all-time lowest historical price for every game.
- **🔐 Secure User Authentication**: User registration and login with bcrypt password hashing and stateless JWT bearer token authentication.
- **🎨 Dark Monochrome UI**: Built with React 19, Tailwind CSS, Lucide icons, and Canvas API animations with reactive depth-of-field blur on search.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/) ORM, SQLite, [HTTPX](https://www.python-httpx.org/), [Pydantic Settings](https://docs.pydantic.dev/).
- **Frontend**: [React 19](https://react.dev/), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/), [Lucide React](https://lucide.dev/), Canvas API.
- **External Services**:
  - [CheapShark API](https://apidocs.cheapshark.com/): Free public gaming deal API (no key or registration needed).
  - [Resend](https://resend.com/): Transactional email delivery service.

---

## 📋 Prerequisites

Before running the application, ensure you have the following installed on your machine:
- **Python**: version `3.10` or higher ([python.org](https://www.python.org/))
- **Node.js**: version `18.x` or higher and `npm` ([nodejs.org](https://nodejs.org/))
- **Git** ([git-scm.com](https://git-scm.com/))

---

## 🚀 Step-by-Step Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Alavars/gamedeal.git
cd gamedeal
```

---

### 2. Configure Python Virtual Environment

Create and activate a virtual environment, then install Python dependencies:

#### On Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### On Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Environment Variables Configuration (`.env`)

Copy the provided `.env.example` file to create your own `.env`:

#### On Windows (PowerShell or CMD):
```powershell
copy .env.example .env
```

#### On Linux / macOS:
```bash
cp .env.example .env
```

#### Environment Variables Explanation:

```env
# Application Settings
APP_NAME=GameDealPulse
APP_ENV=development
APP_PORT=8000
SECRET_KEY=change_this_to_a_secure_random_key_for_jwt_session

# Database (SQLite is created automatically in ./data/app.db)
DATABASE_URL=sqlite:///./data/app.db

# CheapShark API (Public API - NO KEY REQUIRED)
CHEAPSHARK_BASE_URL=https://www.cheapshark.com/api/1.0

# Email Alerts (OPTIONAL)
RESEND_API_KEY=your_resend_api_key_here
SENDER_EMAIL=onboarding@resend.dev
```

> [!TIP]
> **Do I need external API keys to test this project?**
> - **CheapShark API**: **No API key required!** It is a free, open public API.
> - **Resend API**: **Optional!** If you want real emails delivered to your inbox, get a free key from [resend.com](https://resend.com) (starts with `re_`). If left blank or as default, the application automatically enters **Mock Mode** and prints all email alerts to the server console.

---

### 4. Install Frontend Dependencies & Build

Install the frontend packages and compile the production client bundle:

```bash
cd frontend
npm install
npm run build
cd ..
```

---

### 5. Run the Application

Start the FastAPI application. The backend automatically serves the compiled React single-page application at the root URL:

```bash
python -m uvicorn src.main:app --reload --port 8000
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 💻 Frontend Development Mode (Optional)

If you wish to make live modifications to the React UI with Hot Module Replacement (HMR):

1. Keep the FastAPI server running on port `8000`:
   ```bash
   python -m uvicorn src.main:app --reload --port 8000
   ```
2. In a separate terminal, launch the Vite development server:
   ```bash
   cd frontend
   npm run dev
   ```
3. Open **[http://localhost:5173](http://localhost:5173)** in your browser (Vite dev server proxies API calls to FastAPI).

---

## 🧪 Running Automated Tests

To run the automated API test suite (tests health check, CORS, authentication register/login, deal search, and wishlist CRUD):

```bash
python tests/test_api_endpoints.py
```

---

## 📁 Project Structure

```text
gamedeal/
├── src/
│   ├── database/             # SQLAlchemy connection & models (User, Game, WishlistItem)
│   ├── routes/               # FastAPI route controllers
│   │   ├── auth.py           # User registration, login, and JWT /auth/me
│   │   ├── deals.py          # CheapShark search, top deals, game details
│   │   └── wishlist.py       # Wishlist CRUD and test alert trigger
│   ├── schemas/              # Pydantic data validation schemas
│   ├── services/             # Core business logic
│   │   ├── cheapshark.py     # CheapShark API client with Steam CDN normalization
│   │   ├── mailer.py         # Resend email dispatcher with mock fallback
│   │   ├── scheduler.py      # Automated price tracking background task
│   │   └── analytics.py      # Price metrics and discount calculations
│   ├── utils/                # Password hashing (bcrypt) and JWT token helpers
│   ├── config.py             # Pydantic Settings configuration loader
│   └── main.py               # FastAPI entry point & static SPA mounting
├── frontend/                 # React 19 + Vite Single Page Application
│   ├── src/
│   │   ├── components/       # UI components (GameCard, GameModal, Wishlist, Artwork)
│   │   │   ├── originkit/    # Two Reaching Hands generative canvas component
│   │   │   ├── GameCard.jsx  # Deal card with price badge and direct store link
│   │   │   ├── GameImage.jsx # Resilient cover image with Gamepad fallback
│   │   │   └── GameModal.jsx # Comprehensive game analytics & price history modal
│   │   ├── api.js            # Axios/Fetch API client with auth token interceptor
│   │   └── App.jsx           # Main React root application
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite bundler configuration
├── data/                     # Local SQLite database directory (git-ignored)
├── tests/                    # Automated test suites
├── .env.example              # Template environment configuration file
├── .gitignore                # Git ignore rules for secrets and build artifacts
├── requirements.txt          # Python dependencies
└── README.md                 # English documentation & quickstart guide
```

---

## 🔒 Security & Privacy

- **API Keys & Secrets**: The `.env` file and all sensitive credentials are listed in `.gitignore` and excluded from source control.
- **Password Security**: Passwords are never stored in plaintext; they are hashed using `bcrypt`.
- **Stateless Auth**: User sessions are authenticated via stateless JWT (JSON Web Tokens).
- **SQLite Database**: Local database files (`*.db`) are ignored by Git to avoid leaking personal data.

---

## 📄 License

This project is created for educational and demonstration purposes. All game data, titles, and trademarks are property of their respective publishers and storefronts.
