# handlers/affix_manage_handler.py

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.access_control import is_admin
from core.affix_loader import (
    prefix_dict,
    add_prefix,
    remove_prefix,
    add_word_to_prefix,
    remove_word_from_prefix,
    suffix_dict,
    add_suffix,
    remove_suffix,
    add_word_to_suffix,
    remove_word_from_suffix,
)

# Prefix commands

def addprefix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can add prefixes.")
    args = context.args
    if not args:
        return update.message.reply_text("❗ Usage: /addprefix <prefix1> [prefix2] …")
    added, failed = [], []
    for p in args:
        try:
            add_prefix(p)
            added.append(p.lower())
        except ValueError as e:
            failed.append(f"{p.lower()} ({e})")
    resp = []
    if added:
        resp.append(f"✅ Prefixes added: {', '.join(added)}")
    if failed:
        resp.append(f"❌ Could not add: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def rmprefix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can remove prefixes.")
    args = context.args
    if not args:
        return update.message.reply_text("❗ Usage: /rmprefix <prefix1> [prefix2] …")
    removed, failed = [], []
    for p in args:
        try:
            remove_prefix(p)
            removed.append(p.lower())
        except ValueError as e:
            failed.append(f"{p.lower()} ({e})")
    resp = []
    if removed:
        resp.append(f"🗑️ Prefixes removed: {', '.join(removed)}")
    if failed:
        resp.append(f"❌ Could not remove: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def caddprefix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can add words to a prefix.")
    args = context.args
    if len(args) < 2:
        return update.message.reply_text("❗ Usage: /caddprefix <prefix> <word1> [word2] …")
    prefix, words = args[0], args[1:]
    added, failed = [], []
    for w in words:
        try:
            add_word_to_prefix(prefix, w)
            added.append(w.lower())
        except ValueError as e:
            failed.append(f"{w.lower()} ({e})")
    resp = []
    if added:
        resp.append(f"✅ Under '{prefix}': added {', '.join(added)}")
    if failed:
        resp.append(f"❌ Could not add: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def crmprefix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can remove words from a prefix.")
    args = context.args
    if len(args) < 2:
        return update.message.reply_text("❗ Usage: /crmprefix <prefix> <word1> [word2] …")
    prefix, words = args[0], args[1:]
    removed, failed = [], []
    for w in words:
        try:
            remove_word_from_prefix(prefix, w)
            removed.append(w.lower())
        except ValueError as e:
            failed.append(f"{w.lower()} ({e})")
    resp = []
    if removed:
        resp.append(f"🗑️ Under '{prefix}': removed {', '.join(removed)}")
    if failed:
        resp.append(f"❌ Could not remove: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def twprefix_cmd(update: Update, context: CallbackContext):
    if not context.args:
        return update.message.reply_text("❗ Usage: /twprefix <prefix>")
    p = context.args[0].lower()
    total = len(prefix_dict.get(p, []))
    update.message.reply_text(f"📊 Total words under '{p}': {total}")

def listprefixes_cmd(update: Update, context: CallbackContext):
    keys = list(prefix_dict.keys())
    text = "🔤 Prefix categories:\n" + ("\n".join(f"• {k}" for k in keys) if keys else "ℹ️ None yet.")
    update.message.reply_text(text)

# Suffix commands

def addsuffix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can add suffixes.")
    args = context.args
    if not args:
        return update.message.reply_text("❗ Usage: /addsuffix <suffix1> [suffix2] …")
    added, failed = [], []
    for s in args:
        try:
            add_suffix(s)
            added.append(s.lower())
        except ValueError as e:
            failed.append(f"{s.lower()} ({e})")
    resp = []
    if added:
        resp.append(f"✅ Suffixes added: {', '.join(added)}")
    if failed:
        resp.append(f"❌ Could not add: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def rmsuffix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can remove suffixes.")
    args = context.args
    if not args:
        return update.message.reply_text("❗ Usage: /rmsuffix <suffix1> [suffix2] …")
    removed, failed = [], []
    for s in args:
        try:
            remove_suffix(s)
            removed.append(s.lower())
        except ValueError as e:
            failed.append(f"{s.lower()} ({e})")
    resp = []
    if removed:
        resp.append(f"🗑️ Suffixes removed: {', '.join(removed)}")
    if failed:
        resp.append(f"❌ Could not remove: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def caddsuffix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can add words to a suffix.")
    args = context.args
    if len(args) < 2:
        return update.message.reply_text("❗ Usage: /caddsuffix <suffix> <word1> [word2] …")
    suffix, words = args[0], args[1:]
    added, failed = [], []
    for w in words:
        try:
            add_word_to_suffix(suffix, w)
            added.append(w.lower())
        except ValueError as e:
            failed.append(f"{w.lower()} ({e})")
    resp = []
    if added:
        resp.append(f"✅ Under '{suffix}': added {', '.join(added)}")
    if failed:
        resp.append(f"❌ Could not add: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def crmsuffix_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Only Owner/Sudo can remove words from a suffix.")
    args = context.args
    if len(args) < 2:
        return update.message.reply_text("❗ Usage: /crmsuffix <suffix> <word1> [word2] …")
    suffix, words = args[0], args[1:]
    removed, failed = [], []
    for w in words:
        try:
            remove_word_from_suffix(suffix, w)
            removed.append(w.lower())
        except ValueError as e:
            failed.append(f"{w.lower()} ({e})")
    resp = []
    if removed:
        resp.append(f"🗑️ Under '{suffix}': removed {', '.join(removed)}")
    if failed:
        resp.append(f"❌ Could not remove: {', '.join(failed)}")
    update.message.reply_text("\n".join(resp))

def twsuffix_cmd(update: Update, context: CallbackContext):
    if not context.args:
        return update.message.reply_text("❗ Usage: /twsuffix <suffix>")
    s = context.args[0].lower()
    total = len(suffix_dict.get(s, []))
    update.message.reply_text(f"📊 Total words under '{s}': {total}")

def listsuffixes_cmd(update: Update, context: CallbackContext):
    keys = list(suffix_dict.keys())
    text = "🔤 Suffix categories:\n" + ("\n".join(f"• {k}" for k in keys) if keys else "ℹ️ None yet.")
    update.message.reply_text(text)

def register(dp):
    dp.add_handler(CommandHandler("addprefix", addprefix_cmd))
    dp.add_handler(CommandHandler("rmprefix", rmprefix_cmd))
    dp.add_handler(CommandHandler("caddprefix", caddprefix_cmd))
    dp.add_handler(CommandHandler("crmprefix", crmprefix_cmd))
    dp.add_handler(CommandHandler("twprefix", twprefix_cmd))
    dp.add_handler(CommandHandler("listprefixes", listprefixes_cmd))
    dp.add_handler(CommandHandler("addsuffix", addsuffix_cmd))
    dp.add_handler(CommandHandler("rmsuffix", rmsuffix_cmd))
    dp.add_handler(CommandHandler("caddsuffix", caddsuffix_cmd))
    dp.add_handler(CommandHandler("crmsuffix", crmsuffix_cmd))
    dp.add_handler(CommandHandler("twsuffix", twsuffix_cmd))
    dp.add_handler(CommandHandler("listsuffixes", listsuffixes_cmd))