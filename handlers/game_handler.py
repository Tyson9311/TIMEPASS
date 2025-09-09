# handlers/game_handler.py

import time

from telegram import ParseMode, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from apscheduler.jobstores.base import JobLookupError

import config
from utils.access_control import is_admin
from core.game_session import sessions
from core.score_manager import record_game_end
from utils.message_builder import build_turn_prompt
from core.txt_dictionary import load_words, load_nh
from core.affix_loader import prefix_dict, suffix_dict


def _schedule_turn_timeout(context: CallbackContext, cid: int):
    sess = sessions.get(cid)
    if not sess:
        return

    # cancel any existing timeout job
    if sess.elimination_job:
        try:
            sess.elimination_job.schedule_removal()
        except (JobLookupError, Exception):
            pass

    sess.turn_start_time = time.time()
    current_uid = sess.order[0]
    job = context.job_queue.run_once(
        _turn_timeout,
        config.TURN_TIMER,
        context={"chat_id": cid, "user_id": current_uid}
    )
    sess.elimination_job = job


def _turn_timeout(context: CallbackContext):
    data = context.job.context
    cid  = data["chat_id"]
    uid  = data["user_id"]
    sess = sessions.get(cid)

    if not sess or sess.order[0] != uid:
        return

    name = sess.players[uid]["name"]
    sess.eliminate(uid)
    context.bot.send_message(
        cid,
        f"⏰ Time’s up for [{name}](tg://user?id={uid})! Eliminated.",
        parse_mode=ParseMode.MARKDOWN
    )

    # end game if one remains
    if len(sess.order) == 1:
        winner = sess.order[0]
        wname  = sess.players[winner]["name"]
        record_game_end(list(sess.players.keys()), winner)
        context.bot.send_message(
            cid,
            f"🎉 Game over! Winner: [{wname}](tg://user?id={winner})",
            parse_mode=ParseMode.MARKDOWN
        )
        del sessions[cid]
        return

    # otherwise prompt next turn
    prompt = build_turn_prompt(sess)
    context.bot.send_message(cid, prompt, parse_mode=ParseMode.MARKDOWN)
    _schedule_turn_timeout(context, cid)


def join_cmd(update: Update, context: CallbackContext):
    cid  = update.effective_chat.id
    uid  = update.effective_user.id
    name = update.effective_user.first_name
    sess = sessions.get(cid)

    # only before game start
    if not sess or sess.start_time:
        return

    if sess.add_player(uid, name):
        secs_left = int(sess.join_end_time - time.time())
        update.message.reply_text(
            f"✅ [{name}](tg://user?id={uid}) joined!\n⏳ {secs_left}s left",
            parse_mode=ParseMode.MARKDOWN
        )


def exit_cmd(update: Update, context: CallbackContext):
    cid = update.effective_chat.id
    uid = update.effective_user.id
    sess = sessions.get(cid)

    # only before game start
    if sess and not sess.start_time and sess.remove_player(uid):
        update.message.reply_text("🚪 You have left the lobby.")


def forcestop_cmd(update: Update, context: CallbackContext):
    """
    Force-stop at any time: cancels all jobs for this chat and deletes session.
    Always sends a confirmation message.
    """
    print("✅ forcestop_cmd triggered")

    cid = update.effective_chat.id
    uid = update.effective_user.id

    if not is_admin(uid):
        if update.message:
            return update.message.reply_text("🚫 Only Owner/Sudo can force stop.")
        else:
            context.bot.send_message(cid, "🚫 Only Owner/Sudo can force stop.")
            return

    sess = sessions.pop(cid, None)
    if not sess:
        if update.message:
            return update.message.reply_text("ℹ️ No active game to stop here.")
        else:
            context.bot.send_message(cid, "ℹ️ No active game to stop here.")
            return

    # Cancel all jobs linked to this chat
    for job in context.job_queue.get_jobs():
        ctx = getattr(job, "context", None)
        if isinstance(ctx, dict) and ctx.get("chat_id") == cid:
            try:
                job.schedule_removal()
            except (JobLookupError, Exception):
                pass

    sess.join_jobs.clear()
    sess.elimination_job = None

    # ✅ Always send confirmation
    if update.message:
        update.message.reply_text("🛑 Game forcibly stopped.", parse_mode=ParseMode.MARKDOWN)
    else:
        context.bot.send_message(cid, "🛑 Game forcibly stopped.", parse_mode=ParseMode.MARKDOWN)


def submission_handler(update: Update, context: CallbackContext):
    cid = update.effective_chat.id
    uid = update.effective_user.id

    # 🛡️ Guard: ignore non-text messages
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower()
    sess = sessions.get(cid)

    # ...rest of your logic...

    # ignore if no active game
    if not sess or not sess.start_time:
        return

    # out-of-turn guard
    if uid != sess.order[0]:
        return update.message.reply_text(
            "❌ Not your turn. Please wait.",
            parse_mode=ParseMode.MARKDOWN
        )

    # validate word
    valid = False
    mode  = sess.current_mode_type
    param = sess.current_mode_param or ""

    if mode == "category":
        valid = text in set(load_words(param))
    elif mode in ("normal", "hard"):
        valid = text in set(load_nh())
    elif mode == "prefix":
        valid = text in set(prefix_dict.get(param, []))
    elif mode == "suffix":
        valid = text in set(suffix_dict.get(param, []))

    if not valid:
        return update.message.reply_text(
            "❌ Invalid answer. Please try again.",
            parse_mode=ParseMode.MARKDOWN
        )

    # cancel existing timeout
    if sess.elimination_job:
        try:
            sess.elimination_job.schedule_removal()
        except (JobLookupError, Exception):
            pass

    # advance turn
    sess.last_word         = text
    sess.total_submissions += 1
    sess.next_turn()

    # check for win
    if len(sess.order) == 1:
        winner = sess.order[0]
        wname  = sess.players[winner]["name"]
        record_game_end(list(sess.players.keys()), winner)
        del sessions[cid]
        return update.message.reply_text(
            f"🎉 Game over! Winner: [{wname}](tg://user?id={winner})",
            parse_mode=ParseMode.MARKDOWN
        )

    # prompt next
    prompt = build_turn_prompt(sess)
    update.message.reply_text(prompt, parse_mode=ParseMode.MARKDOWN)
    _schedule_turn_timeout(context, cid)


def register(dp):
    dp.add_handler(CommandHandler("join", join_cmd))
    dp.add_handler(CommandHandler("exit", exit_cmd))
    dp.add_handler(CommandHandler("forcestop", forcestop_cmd))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, submission_handler))

