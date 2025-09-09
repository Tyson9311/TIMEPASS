# handlers/role_handler.py

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from utils.access_control import is_owner, is_sudo, is_banned

def role_cmd(update: Update, context: CallbackContext):
    """
    /role → shows ID, name, username and assigned role(s).
    Escapes Markdown special chars and uses Markdown V2 parsing.
    """
    user = update.effective_user
    uid  = user.id
    name = user.first_name or "<no first name>"
    uname = f"@{user.username}" if user.username else "N/A"

    # determine role
    roles = []
    if is_owner(uid):
        roles.append("Owner")
    elif is_sudo(uid):
        roles.append("Sudo")
    if is_banned(uid):
        roles.append("Banned")
    if not roles:
        roles.append("User")

    raw = (
        f"👤 *Your Role Details*\n\n"
        f"• ID       : `{uid}`\n"
        f"• Name     : {name}\n"
        f"• Username : {uname}\n"
        f"• Role     : {', '.join(roles)}"
    )

    # Escape any Markdown V2 special characters
    safe = escape_markdown(raw, version=2)
    update.message.reply_text(safe, parse_mode=ParseMode.MARKDOWN_V2)

def register(dp):
    dp.add_handler(CommandHandler("role", role_cmd))
