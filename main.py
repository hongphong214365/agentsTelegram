import sys
import telebot
from config import TOKEN, validate_environment
from handlers import register_handlers
from log import logger, startup_log


def _redact_token(message: str) -> str:
    if not TOKEN:
        return message
    return message.replace(TOKEN, "[REDACTED]")


def main():
    startup_log()
    logger.info("Initializing bot and checking environment...")

    is_ok, errors = validate_environment()
    if not is_ok:
        for err in errors:
            logger.critical(f"Environment check failed: {err}")
        print("Environment check failed. Check log for details.")
        sys.exit(1)

    logger.info("Environment check passed.")

    try:
        bot = telebot.TeleBot(TOKEN)
        bot_info = bot.get_me()
        logger.info(
            f"Connection verified. Bot authorized as @{bot_info.username} (ID: {bot_info.id})."
        )
    except telebot.apihelper.ApiTelegramException as e:
        safe_error = _redact_token(str(e))
        logger.critical(
            f"Authentication failed: Telegram token is invalid, disabled, or revoked ({safe_error})."
        )
        print(f"Authentication failed: {safe_error}")
        sys.exit(1)
    except Exception as e:
        safe_error = _redact_token(str(e))
        logger.critical(
            f"Network connection failed: Unable to connect to Telegram API ({safe_error})."
        )
        print(f"Network error: {safe_error}")
        sys.exit(1)

    register_handlers(bot)
    logger.info("Bot handlers registered. Starting polling...")
    print("Telegram agent started successfully.")

    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
        print("Bot stopped.")
    except Exception as e:
        safe_error = _redact_token(str(e))
        logger.critical(f"Bot terminated unexpectedly: {safe_error}")
        print(f"Bot terminated unexpectedly: {safe_error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
