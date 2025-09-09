# handlers/mode_handler.py

import time
import random
import string

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext

import config
from utils.access_control import is_banned
from utils.group_control import is_permitted
from core.game_session import sessions, GameSession
from core.txt_dictionary import load_words
from core.affix_loader import prefix_dict, suffix_dict
from utils.message_builder import build_turn_prompt

# import the scheduler helper from game_handler
from handlers.game_handler import _schedule_turn_timeout

def _join_alert(context: CallbackContext):
    left = context.job.context["left"]
    cid  = context.job.context["chat_id"]
    context.bot.send_message(cid, f"⏳ {left}s left to join the game.")

def _auto_start(context: CallbackContext):
    cid  = context.job.context
    sess = sessions.get(cid)
    if not sess or sess.start_time:
        return

    # start the game
    sess.start()
    prompt = build_turn_prompt(sess)
    context.bot.send_message(
        cid,
        f"🎮 Game has started!\n\n{prompt}",
        parse_mode=ParseMode.MARKDOWN
    )

    # schedule the first turn timeout
    _schedule_turn_timeout(context, cid)

def _start_mode(update: Update, context: CallbackContext, mode: str, param=None):
    cid     = update.effective_chat.id
    user_id = update.effective_user.id

    if is_banned(user_id):
        return update.message.reply_text("🚫 You are banned.")
    if not is_permitted(cid):
        return update.message.reply_text("🚫 Group not permitted.")
    if cid in sessions:
        return update.message.reply_text("⚠️ A game is already active.")

    sess = GameSession(cid)
    sess.current_mode_type  = mode
    sess.current_mode_param = param

    text = f"🎯 Starting {mode.title()} mode!"
    if mode == "category":
        letter = random.choice(string.ascii_lowercase)
        sess.start_letter = letter
        text += f"\nFirst letter: `{letter.upper()}`"
    elif mode in ("prefix", "suffix"):
        dct = prefix_dict if mode == "prefix" else suffix_dict
        key = random.choice(list(dct.keys()))
        sess.current_mode_param = key
        text += f"\n{mode.title()}: `{key}`"

    text += "\nUse /join to enter the Arena."
    text += f"\nYou have *{config.JOIN_TIMEOUT}s* to join."
    sessions[cid] = sess

    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    # schedule join-phase alerts and auto-start
    now = time.time()
    sess.join_end_time = now + config.JOIN_TIMEOUT

    for left in config.JOIN_ALERT_INTERVALS:
        when = config.JOIN_TIMEOUT - left
        if when > 0:
            job = context.job_queue.run_once(
                _join_alert,
                when,
                context={"chat_id": cid, "left": left}
            )
            sess.join_jobs.append(job)

    job = context.job_queue.run_once(_auto_start, config.JOIN_TIMEOUT, context=cid)
    sess.join_jobs.append(job)

def register(dp):
    dp.add_handler(CommandHandler("chemistry",   lambda u, c: _start_mode(u, c, "category", "chemistry")))
    dp.add_handler(CommandHandler("biology",     lambda u, c: _start_mode(u, c, "category", "biology")))
    dp.add_handler(CommandHandler("physics",     lambda u, c: _start_mode(u, c, "category", "physics")))
    dp.add_handler(CommandHandler("cities",      lambda u, c: _start_mode(u, c, "category", "cities")))
    dp.add_handler(CommandHandler("country",     lambda u, c: _start_mode(u, c, "category", "country")))
    dp.add_handler(CommandHandler("animal",      lambda u, c: _start_mode(u, c, "category", "animal")))
    dp.add_handler(CommandHandler("flowers",     lambda u, c: _start_mode(u, c, "category", "flowers")))
    dp.add_handler(CommandHandler("mathematics", lambda u, c: _start_mode(u, c, "category", "mathematics")))
    dp.add_handler(CommandHandler("prefix",      lambda u, c: _start_mode(u, c, "prefix")))
    dp.add_handler(CommandHandler("suffix",      lambda u, c: _start_mode(u, c, "suffix")))
    dp.add_handler(CommandHandler("normal",      lambda u, c: _start_mode(u, c, "normal")))
    dp.add_handler(CommandHandler("hard",        lambda u, c: _start_mode(u, c, "hard")))
