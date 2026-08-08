# agentsTelegram

A simple Telegram bot to run Python files remotely and return output or errors.

[Tiếng Việt](README.md)

## Features

* Run Python files remotely via Telegram.
* Receive program output directly in Telegram.
* Error notifications on execution failure.
* Restricted access using a Telegram Admin ID.

## Requirements

* Python 3.10 or newer
* Telegram Bot Token

## Installation

### Method 1: Using uv (Recommended)

```bash
# Create virtual environment and install dependencies
uv venv
uv sync

# Run the bot
uv run main.py
```

### Method 2: Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## Configuration

Set the following environment variables:

* `TELEGRAM_TOKEN`: Your bot token from @BotFather.
* `TELEGRAM_ADMIN_ID`: Your numeric Telegram ID.

## Commands

* `/start` - Displays instructions.
* `/ping` - Checks bot status.
* `/run <file.py>` - Executes a Python file (Admin only).
* `/log` - Shows the last 20 log lines (Admin only).
* `/status` - Shows bot status.

## Security Notes

* Never share or commit your `TELEGRAM_TOKEN`.
* Use environment variables to manage sensitive data.

## License

MIT License
