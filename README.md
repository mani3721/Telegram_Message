# Telethon API Project

A Python project using the Telethon library to interact with the Telegram API.

## Features

- Telegram client functionality
- Message handling
- File operations
- Web API interface with FastAPI
- Environment-based configuration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Telethon API"
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

2. Fill in your Telegram API credentials:
```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
PHONE_NUMBER=your_phone_number
```

## Usage

### Running the Telegram Client
```bash
python src/telegram_client.py
```

### Running the Web API
```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

## Project Structure

```
Telethon API/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── telegram_client.py
│   ├── models.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_telegram_client.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /health` - Health check
- `POST /send-message` - Send a message
- `GET /get-messages` - Get messages from a chat
- `POST /upload-file` - Upload a file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License 