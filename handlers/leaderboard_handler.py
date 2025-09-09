from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext
from core.score_manager import get_leaderboard

def leaderboard_cmd(update: Update, context: CallbackContext):
    board = get_leaderboard()
    lines = ["🏆 Leaderboard (Top 10)"]
    for idx, (uid, gp, w, rate) in enumerate(board, start=1):
        mention = f"[User](tg://user?id={uid})"
        lines.append(f"{idx}. {mention} — {w} wins, {gp} games, {rate:.1f}% win rate")
    update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

def register(dp):
    dp.add_handler(CommandHandler("leaderboard", leaderboard_cmd))