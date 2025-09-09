from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.access_control import is_admin
import config

def settimer_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Owner/Sudo only.")
    if not context.args or not context.args[0].isdigit():
        return update.message.reply_text("❗ Usage: /settimer <seconds>")
    sec = int(context.args[0])
    config.TURN_TIMER = sec
    update.message.reply_text(f"⏱️ Turn timer set to {sec}s.")

def setminlength_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Owner/Sudo only.")
    if not context.args or not context.args[0].isdigit():
        return update.message.reply_text("❗ Usage: /setminlength <length>")
    config.MIN_LENGTH = int(context.args[0])
    update.message.reply_text(f"🔢 Min length set to {config.MIN_LENGTH}.")

def setmaxplayers_cmd(update: Update, context: CallbackContext):
    if not is_admin(update.effective_user.id):
        return update.message.reply_text("🚫 Owner/Sudo only.")
    if not context.args or not context.args[0].isdigit():
        return update.message.reply_text("❗ Usage: /setmaxplayers <count>")
    config.MAX_PLAYERS = int(context.args[0])
    update.message.reply_text(f"👥 Max players set to {config.MAX_PLAYERS}.")

def register(dp):
    dp.add_handler(CommandHandler("settimer", settimer_cmd))
    dp.add_handler(CommandHandler("setminlength", setminlength_cmd))
    dp.add_handler(CommandHandler("setmaxplayers", setmaxplayers_cmd))