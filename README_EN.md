# AgentsTelegram: Remote Computer Control with Telegram

A Telegram bot that runs on your computer. Send commands through Telegram and receive their results on the device you are using.

[Tiếng Việt](README.md)

## Features

* Run Python files remotely through Telegram.
* Adjust settings such as execution timeout, log line count, and log level.
* Restrict administrative commands to the configured Telegram user ID.
* Send execution output or error messages back through Telegram to your phone, another PC, or other devices.
* Record activity and view, filter, change the level of, or clear logs.

## Requirements

* Python 3.14.
* A Telegram bot token.
* An Internet connection so the bot can communicate with Telegram.
* Your Telegram user ID to restrict access.

## Installation

### Method 1: Using uv (recommended)

```bash
# Create a virtual environment and install dependencies
uv venv
uv sync

# Run the bot
uv run main.py
```

### Method 2: Using pip

Create a virtual environment:

```bash
python -m venv .venv
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install dependencies and run the bot:

```bash
pip install -r setup/requirements.txt
python main.py
```

## Configuration

### 1. Create a bot and get its token

Open Telegram and message [@BotFather](https://t.me/BotFather). Create a bot with `/newbot` and follow the instructions. Keep the token provided by BotFather private.

### 2. Get your Telegram user ID

Get the **numeric ID of your personal Telegram account** from a trusted Telegram ID lookup bot. Do not use your username, display name, or the bot's ID in place of your user ID.

### 3. Set the two environment variables

The application reads only these two environment variables:

* `TELEGRAM_TOKEN`: the bot token from BotFather.
* `TELEGRAM_ADMIN_ID`: your numeric Telegram user ID.

Replace the sample values below with your own. These commands set the variables for the current terminal session only.

**Windows (CMD):**

```cmd
set TELEGRAM_TOKEN=your_bot_token
set TELEGRAM_ADMIN_ID=123456789
```

**Windows (PowerShell):**

```powershell
$env:TELEGRAM_TOKEN = "your_bot_token"
$env:TELEGRAM_ADMIN_ID = "123456789"
```

**macOS:**

```bash
export TELEGRAM_TOKEN="your_bot_token"
export TELEGRAM_ADMIN_ID="123456789"
```

**Linux:**

```bash
export TELEGRAM_TOKEN="your_bot_token"
export TELEGRAM_ADMIN_ID="123456789"
```

Run the bot from the same terminal where you set the variables. For persistent configuration, add the variables to your operating system's private environment settings; never put the token in source code or commit it to Git.

### 4. Adjust other settings (optional)

In `config.py`, you can change `RUN_TIMEOUT` (30 seconds by default), `LOG_LINES` (20 by default), `LOG_FILE` (defaults to `temp/agent.log`), and `LEVEL` (defaults to `INFO`). Stop and restart the bot to apply changes.

## Using the bot

### Run the bot

Open a terminal in the project directory, set the two environment variables as described above, and run:

```bash
uv run main.py
```

If you installed with pip, activate the virtual environment and run `python main.py`. On successful startup, the bot prints:

```text
Telegram agent started successfully.
```

### Supported commands

* `/start` — Welcome message and usage instructions.
* `/run filename.py` — Run a `.py` file in the current project directory; the output or error is sent back through Telegram. Execution is limited by `RUN_TIMEOUT`, with a 15-second cooldown between runs to prevent spam.
* `/log` — Show the last 20 log lines by default. Only the configured administrator can use it.
* `/status` — Show the current directory, Python version, log file path, and execution timeout (**experimental**).
* `/ping` — Quick connectivity check; the bot replies `online`.

`/log` options (send them in the same message as `/log`):

| Syntax | Purpose |
| --- | --- |
| `/log 50`, `/log -lines=50`, `/log --lines=50`, `/log -n=50` | Show the requested number of last lines; the minimum is 1. |
| `/log -level=ERROR` or `/log --level=ERROR` | Filter by level, for example `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. |
| `/log -time=11:09` or `/log --time=11:09` | Filter by a time string found in the log timestamp. |
| `/log -get-level`, `/log --get-level`, `/log -current-level`, `/log --current-level` | Show the current log level. |
| `/log -set-level=DEBUG` or `/log --set-level=DEBUG` | Change the log level while the bot is running. |
| `/log -clean` or `/log --clean` | Clear the log file contents. |

Viewing, filtering, changing the level, and clearing logs all require the configured administrator Telegram user ID.

Note: `/ping` currently replies to any Telegram account; all other commands only process requests from the configured ID.

## Security warnings

> **CRITICAL WARNING: YOUR TELEGRAM TOKEN CAN GIVE FULL CONTROL OF YOUR BOT.**
>
> **NEVER share your token in any form:** do not push it to GitHub, send it to friends, post a screenshot that shows it, paste it in a public place, or send it in a chat. Anyone with the token may take control of your bot. If it is exposed, revoke it and create a new token through BotFather immediately. You are responsible for protecting your token and for the consequences of exposing it.

* Do not send your token or logs containing sensitive information to anyone.
* Set `TELEGRAM_ADMIN_ID` to the correct personal ID and share the bot only with people you trust.
* `/run` executes Python code on the computer hosting the bot. Run the bot only on a computer you control, and send commands only from the configured account.
* Do not run `.py` files from unknown sources; malicious code may read, modify, or delete data available to the operating system account running the bot.
* Keep Python and its dependencies up to date, and protect the computer and its operating system account with an appropriate password.

## License

MIT License. See [LICENSE](LICENSE).
