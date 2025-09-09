from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.access_control import is_admin
from core.txt_dictionary import load_words, save_words

MODES = [
    "chemistry", "biology", "physics", "cities",
    "country", "animal", "flowers", "mathematics"
]

def _make_add(mode: str):
    def cmd(update: Update, context: CallbackContext):
        if not is_admin(update.effective_user.id):
            return update.message.reply_text("🚫 Owner/Sudo only.")
        args = context.args
        if not args:
            return update.message.reply_text(f"❗ Usage: /add{mode} <w1> [w2]…")
        words = load_words(mode)
        added, failed = [], []
        for w in args:
            wkey = w.strip().lower()
            if wkey in words:
                failed.append(f"{wkey}(exists)")
            else:
                words.append(wkey)
                added.append(wkey)
        save_words(mode, words)
        res = []
        if added: res.append(f"✅ Added to {mode}: {', '.join(added)}")
        if failed: res.append(f"❌ Failed: {', '.join(failed)}")
        update.message.reply_text("\n".join(res))
    return cmd

def _make_rm(mode: str):
    def cmd(update: Update, context: CallbackContext):
        if not is_admin(update.effective_user.id):
            return update.message.reply_text("🚫 Owner/Sudo only.")
        args = context.args
        if not args:
            return update.message.reply_text(f"❗ Usage: /rm{mode} <w1> [w2]…")
        words = load_words(mode)
        removed, failed = [], []
        for w in args:
            wkey = w.strip().lower()
            if wkey not in words:
                failed.append(f"{wkey}(nf)")
            else:
                words.remove(wkey)
                removed.append(wkey)
        save_words(mode, words)
        res = []
        if removed: res.append(f"🗑️ Removed: {', '.join(removed)}")
        if failed: res.append(f"❌ Failed: {', '.join(failed)}")
        update.message.reply_text("\n".join(res))
    return cmd

def _make_tw(mode: str):
    def cmd(update: Update, context: CallbackContext):
        total = len(load_words(mode))
        update.message.reply_text(f"📊 Total {mode}: {total}")
    return cmd

def register(dp):
    for m in MODES:
        dp.add_handler(CommandHandler(f"add{m}", _make_add(m)))
        dp.add_handler(CommandHandler(f"rm{m}", _make_rm(m)))
        dp.add_handler(CommandHandler(f"tw{m}", _make_tw(m)))