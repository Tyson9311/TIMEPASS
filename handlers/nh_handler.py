# handlers/nh_handler.py

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.access_control import is_admin
from core.txt_dictionary import add_nh_word, remove_nh_word, count_nh_words

def addnh_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can add words.")
    args = context.args
    if not args:
        return update.message.reply_text("❗ Usage: /addnh <word1> [word2] …")
    added, failed = [], []
    for w in args:
        try:
            add_nh_word(w)
            added.append(w.lower())
        except ValueError as e:
            failed.append(f"{w.lower()} ({e})")
    resp = []
    if added:
        resp.append(f"✅ Added to NH: {', '.join(added)}")
    if failed:
        resp.append(f"❌ Could not add: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def rmnh_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can remove words.")
    args = context.args
    if not args:
        return update.message.reply_text("❗ Usage: /rmnh <word1> [word2] …")
    removed, failed = [], []
    for w in args:
        try:
            remove_nh_word(w)
            removed.append(w.lower())
        except ValueError as e:
            failed.append(f"{w.lower()} ({e})")
    resp = []
    if removed:
        resp.append(f"🗑️ Removed from NH: {', '.join(removed)}")
    if failed:
        resp.append(f"❌ Could not remove: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def twnh_cmd(update: Update, context: CallbackContext):
    total = count_nh_words()
    update.message.reply_text(f"📊 Total words in NH dictionary: {total}")

def register(dp):
    dp.add_handler(CommandHandler("addnh", addnh_cmd))
    dp.add_handler(CommandHandler("rmnh", rmnh_cmd))
    dp.add_handler(CommandHandler("twnh", twnh_cmd))