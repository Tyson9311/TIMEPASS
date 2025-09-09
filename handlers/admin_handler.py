from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext
import config
from utils.access_control import is_owner, is_sudo
from core.score_manager import (
    add_sudo, remove_sudo, list_sudos,
    ban_user, unban_user, list_banned,
    permit_group, revoke_group, list_permitted_groups,
    # broadcast uses list_permitted_groups
)

def sudo_cmd(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        return update.message.reply_text("🚫 Owner only.")
    if not context.args:
        return update.message.reply_text("❗ Usage: /sudo <user_id>")
    uid = context.args[0]
    try:
        add_sudo(uid)
        update.message.reply_text(f"✅ {uid} is now Sudo.")
    except Exception as e:
        update.message.reply_text(f"❌ Could not add Sudo: {e}")

def unsudo_cmd(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        return update.message.reply_text("🚫 Owner only.")
    uid = context.args[0]
    try:
        remove_sudo(uid)
        update.message.reply_text(f"✅ {uid} is no longer Sudo.")
    except Exception as e:
        update.message.reply_text(f"❌ Could not remove Sudo: {e}")

def listsudo_cmd(update: Update, context: CallbackContext):
    sudos = list_sudos()
    text = "👮‍♂️ Sudos: " + ", ".join(sudos) if sudos else "None"
    update.message.reply_text(text)

def botban_cmd(update: Update, context: CallbackContext):
    if not is_sudo(update.effective_user.id):
        return update.message.reply_text("🚫 Sudo only.")
    uid = context.args[0]
    try:
        ban_user(uid)
        update.message.reply_text(f"🚫 {uid} banned.")
    except Exception as e:
        update.message.reply_text(f"❌ Could not ban: {e}")

def unbotban_cmd(update: Update, context: CallbackContext):
    if not is_sudo(update.effective_user.id):
        return update.message.reply_text("🚫 Sudo only.")
    uid = context.args[0]
    try:
        unban_user(uid)
        update.message.reply_text(f"✅ {uid} unbanned.")
    except Exception as e:
        update.message.reply_text(f"❌ Could not unban: {e}")

def listbotbanned_cmd(update: Update, context: CallbackContext):
    banned = list_banned()
    text = "🚫 Banned: " + ", ".join(banned) if banned else "None"
    update.message.reply_text(text)

def permitgroup_cmd(update: Update, context: CallbackContext):
    if not is_sudo(update.effective_user.id):
        return update.message.reply_text("🚫 Sudo only.")
    gid = int(context.args[0])
    try:
        permit_group(gid)
        update.message.reply_text(f"✅ Group {gid} permitted.")
    except Exception as e:
        update.message.reply_text(f"❌ Could not permit group: {e}")

def revokegroup_cmd(update: Update, context: CallbackContext):
    if not is_sudo(update.effective_user.id):
        return update.message.reply_text("🚫 Sudo only.")
    gid = int(context.args[0])
    try:
        revoke_group(gid)
        update.message.reply_text(f"🚫 Group {gid} revoked.")
    except Exception as e:
        update.message.reply_text(f"❌ Could not revoke group: {e}")

def listpermittedgroups_cmd(update: Update, context: CallbackContext):
    groups = list_permitted_groups()
    text = "🔓 Permitted Groups:\n" + "\n".join(str(g) for g in groups) if groups else "None"
    update.message.reply_text(text)

def broadcast_cmd(update: Update, context: CallbackContext):
    if not is_sudo(update.effective_user.id):
        return update.message.reply_text("🚫 Sudo only.")
    text = update.message.text.partition(" ")[2]
    if not text:
        return update.message.reply_text("❗ Usage: /broadcast <message>")
    targets = set(list_permitted_groups()) | {config.OFFICIAL_GROUP_ID, config.OFFICIAL_CHANNEL_ID}
    sent, failed = 0, 0
    for cid in targets:
        try:
            context.bot.send_message(cid, text, parse_mode=ParseMode.MARKDOWN)
            sent += 1
        except:
            failed += 1
    resp = [f"✅ Sent to {sent} chats."]
    if failed: resp.append(f"❌ Failed for {failed} chats.")
    update.message.reply_text("\n".join(resp))

def register(dp):
    dp.add_handler(CommandHandler("sudo", sudo_cmd))
    dp.add_handler(CommandHandler("unsudo", unsudo_cmd))
    dp.add_handler(CommandHandler("listsudo", listsudo_cmd))
    dp.add_handler(CommandHandler("botban", botban_cmd))
    dp.add_handler(CommandHandler("unbotban", unbotban_cmd))
    dp.add_handler(CommandHandler("listbotbanned", listbotbanned_cmd))
    dp.add_handler(CommandHandler("permitgroup", permitgroup_cmd))
    dp.add_handler(CommandHandler("revokegroup", revokegroup_cmd))
    dp.add_handler(CommandHandler("listpermittedgroups", listpermittedgroups_cmd))
    dp.add_handler(CommandHandler("broadcast", broadcast_cmd))