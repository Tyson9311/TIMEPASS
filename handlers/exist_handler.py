# handlers/exist_handler.py

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from core.txt_dictionary import load_words, load_nh
from core.affix_loader import prefix_dict, suffix_dict

# the eight category modes
CATEGORY_MODES = [
    "chemistry",
    "biology",
    "physics",
    "cities",
    "country",
    "animal",
    "flowers",
    "mathematics",
]

def exist_cmd(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        return update.message.reply_text("❗ Usage: /exist <word1> [word2] …")
    
    # preload all dictionaries once
    nh_words       = set(load_nh())
    category_words = {mode: set(load_words(mode)) for mode in CATEGORY_MODES}
    prefix_map     = prefix_dict  # dict: prefix -> [words…]
    suffix_map     = suffix_dict  # dict: suffix -> [words…]
    
    out_lines = []
    for raw in args:
        w = raw.strip().lower()
        found = []
        
        # NH
        if w in nh_words:
            found.append("NH")
        
        # category
        for mode, words in category_words.items():
            if w in words:
                found.append(mode.title())
        
        # prefix categories
        pref_hits = [p for p, words in prefix_map.items() if w in words]
        for p in pref_hits:
            found.append(f"prefix '{p}'")
        
        # suffix categories
        suff_hits = [s for s, words in suffix_map.items() if w in words]
        for s in suff_hits:
            found.append(f"suffix '{s}'")
        
        if found:
            out_lines.append(f"✅ {w}: {', '.join(found)}")
        else:
            out_lines.append(f"❌ {w}: not found in any dictionary")
    
    update.message.reply_text("\n".join(out_lines))

def register(dp):
    dp.add_handler(CommandHandler("exist", exist_cmd))
