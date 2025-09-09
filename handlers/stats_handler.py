from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from core.score_manager import get_stats

def stats_cmd(update: Update, context: CallbackContext):
    uid = str(update.effective_user.id)
    data = get_stats(uid)
    gp   = data.get("games_played", 0)
    w    = data.get("wins", 0)
    rate = (w / gp * 100) if gp else 0
    text = (
        "📈 Your Stats\n\n"
        f"• Games Played : {gp}\n"
        f"• Wins         : {w}\n"
        f"• Win Rate     : {rate:.1f}%"
    )
    update.message.reply_text(text)

def register(dp):
    dp.add_handler(CommandHandler("stats", stats_cmd))