from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, CallbackContext

def start_cmd(update: Update, context: CallbackContext):
    cid = update.effective_chat.id

    # 📸 Hosted image (WordLink logo)
    photo_url = "https://i.postimg.cc/fb5G85y0/IMG-20250907-214237-294.jpg"  # ← Replace with actual direct image link

    # 📝 Immersive welcome caption
    caption = (
        "*🌌 Welcome to WordLinkBot: Where Words Forge Legends!*\n\n"
        "🔗 _Every letter is a link. Every link is a move. Every move is a moment._\n"
        "🧠 Outsmart your rivals in a game of speed, vocabulary, and strategy.\n\n"
        "👥 Join forces or go solo. Eliminate, survive, and rise to the top.\n"
        "🏆 Only one will be crowned the WordLink Champion.\n\n"
        "📌 Commands:\n"
        "• /join — Enter the arena\n"
        "• /exit — Leave the game\n"
        "• /forcestop — End the match instantly\n\n"
        "✨ Stay connected with the WordLink community below:"
    )

    # 🔘 Inline buttons for group and channel
    buttons = [
        [
            InlineKeyboardButton("👥 Join Official Group", url="https://t.me/+ypEmP_fpo81kZjJk"),
            InlineKeyboardButton("📢 Visit Official Channel", url="https://t.me/WordLink_Updates")
        ]
    ]
    markup = InlineKeyboardMarkup(buttons)

    # 🚀 Send photo with caption and buttons
    context.bot.send_photo(
        chat_id=cid,
        photo=photo_url,
        caption=caption,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )

def register(dp):
    dp.add_handler(CommandHandler("start", start_cmd))
