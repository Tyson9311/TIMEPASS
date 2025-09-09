from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext

def rules_cmd(update: Update, context: CallbackContext):
    cid = update.effective_chat.id

    rules_text = (
        "*📜 WordLinkBot Rules & Gameplay Guide*\n\n"
        "*🔧 Bot Usage Rules:*\n"
        "• Be respectful to other players.\n"
        "• Use /join and /exit responsibly.\n"
        "• Avoid spamming commands or disrupting matches.\n"
        "• Admins may use /forcestop to end chaotic sessions.\n\n"
        "*🎮 Game Rules:*\n"
        "• Players take turns linking words — each new word must start with the last letter of the previous word.\n"
        "• No proper nouns, abbreviations, or repeated words.\n"
        "• Timeouts or invalid entries may result in elimination.\n"
        "• The last player standing wins the round.\n\n"
        "🧠 Strategy, speed, and vocabulary are your weapons.\n"
        "Let the word war begin!"
    )

    context.bot.send_message(
        chat_id=cid,
        text=rules_text,
        parse_mode=ParseMode.MARKDOWN
    )

def register(dp):
    dp.add_handler(CommandHandler("rules", rules_cmd))
