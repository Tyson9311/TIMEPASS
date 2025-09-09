# handlers/info_handler.py

import platform
import time
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext

from core.game_session import sessions
from core.score_manager import list_permitted_groups, list_sudos

# record bot start time when this module is loaded
START_TIME = time.time()

def groupinfo_cmd(update: Update, context: CallbackContext):
    chat = update.effective_chat
    title   = chat.title or "Private Chat"
    chat_id = chat.id
    ctype   = chat.type
    try:
        members = context.bot.get_chat_members_count(chat_id)
    except:
        members = "Unknown"
    text = (
        f"📊 *Group Info*\n\n"
        f"• Title   : {title}\n"
        f"• ID      : `{chat_id}`\n"
        f"• Type    : {ctype}\n"
        f"• Members : {members}"
    )
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def botstatus_cmd(update: Update, context: CallbackContext):
    uptime = int(time.time() - START_TIME)
    h, rem = divmod(uptime, 3600)
    m, s   = divmod(rem, 60)
    uptime_str = f"{h}h{m}m{s}s"
    active_games   = len(sessions)
    permitted_grps = len(list_permitted_groups())
    sudo_count     = len(list_sudos())
    text = (
        f"🤖 *Bot Status*\n\n"
        f"• Uptime           : {uptime_str}\n"
        f"• Active Games     : {active_games}\n"
        f"• Permitted Groups : {permitted_grps}\n"
        f"• Sudo Users       : {sudo_count}\n"
        f"• Python Version   : {platform.python_version()}"
    )
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def register(dp):
    dp.add_handler(CommandHandler("groupinfo", groupinfo_cmd))
    dp.add_handler(CommandHandler("botstatus", botstatus_cmd))
