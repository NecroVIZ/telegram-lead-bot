# Telegram Lead Bot

Professional Telegram bot for collecting leads and saving them to Google Sheets. Suitable for small businesses, freelancers, and startups to quickly launch a lead capture system without the cost of complex CRM.

## Key Features

- Interactive interface with buttons and step-by-step form
- Data validation (name, phone, message)
- Lead confirmation before submission
- Save leads to Google Sheets
- Admin notifications in Telegram
- Admin panel with commands and statistics
- Spam protection (limit on number of leads)
- Full event logging
- Graceful shutdown on stop
- Support for multiple administrators
- Deep linking for tracking sources
- Complete set of automated tests

## Technologies

- Python 3.10+
- aiogram 3.x (FSM, Callbacks, Middleware)
- Google Sheets API (gspread, google-auth)
- dotenv for configuration management
- pytest for testing
- logging with log rotation

## Project Structure

```
telegram-lead-bot/
├── bot/                    # Main bot module
│   ├── handlers/           # Command and message handlers
│   ├── states/             # State machine (FSM)
│   ├── keyboards/          # Keyboards and buttons
│   ├── middleware/         # Middleware
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration from .env
│   └── bot.py              # Handler registration
├── data/                   # Data handling (Google Sheets)
├── logs/                   # Bot logs
├── tests/                  # Automated tests
├── main.py                 # Entry point
├── .env                    # Environment variables
├── .gitignore              # Ignored files
├── requirements.txt        # Dependencies
├── README.md               # This documentation
├── Procfile                # For deployment (Render)
└── pytest.ini             # Test configuration
```

## Installation and Running

### 1. Clone the repository

```bash
git clone https://github.com/your_username/telegram-lead-bot.git
cd telegram-lead-bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Telegram bot

1. Find [@BotFather](https://t.me/BotFather) in Telegram
2. Send `/newbot` and follow the instructions
3. Copy the received **token**

### 5. Configure Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable **Google Sheets API** and **Google Drive API**
4. Create a **service account**:
   - IAM & Admin → Service Accounts → Create Service Account
   - Give it the **Editor** role
5. Create a **JSON key** for the service account
6. Rename the key to `creds.json` and place it in the project root
7. Create a Google Sheet
8. Give access to the sheet to the service account (email from the JSON key)

### 6. Configuration

Create a `.env` file in the project root:

```env
# Telegram bot token (required)
BOT_TOKEN=your_bot_token

# Administrator IDs (comma separated, required)
ADMIN_IDS=123456789,987654321

# Path to Google JSON key (optional, defaults to creds.json)
GOOGLE_CREDS_PATH=creds.json
```

### 7. Run the bot

```bash
python main.py
```

## Testing

To run automated tests:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run tests without warnings
pytest -v --disable-warnings
```

## Bot Commands

| Command     | Description                        |
|-------------|---------------------------------|
| `/start`    | Start working with the bot          |
| `/cancel`   | Cancel the current form         |
| `/help`     | Show help               |
| `/admin`    | Admin panel (admins only) |
| `/stats`    | Lead statistics (admins only) |

## Security

- All sensitive data (tokens, keys) is stored in `.env`
- The `.env` file is added to `.gitignore`
- Limit on number of leads (3 per hour) for spam protection
- Validation of all input data
- Logging without personal data
- Callback security checks

## Scaling

The bot is ready for production and can be:
- Deployed to cloud platforms (Render, Heroku, VPS)
- Extended functionality (payment, calendar, CRM integrations)
- Used as a basis for a SaaS product

## License

MIT License - you can use this code in your projects with attribution.

## Support

If you have questions or issues, create an issue in the GitHub repository.
