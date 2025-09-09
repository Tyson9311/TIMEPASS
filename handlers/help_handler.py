# handlers/help_handler.py

from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext

HELP_TEXT = """
Available commands:
/start – Show welcome message and official links
/help – Show this help message

Mode starters:
/chemistry, /biology, /physics, /cities, /country, /animal, /flowers, /mathematics
/prefix, /suffix, /normal, /hard

Lobby & game control:
/join – Join the current game lobby
/exit – Leave the lobby before start
/forcestart – Force immediate game start (Owner/Sudo)
/forcestop – Stop the current game (Owner/Sudo)

Word submission & rules: simply send your word when it’s your turn  
(Invalid submissions get a second-chance prompt.)

Dictionary management (Owner/Sudo):
/addchemistry, /rmchemistry, /twchemistry  
/addbiology, /rmbiology, /twbiology  
/addphysics, /rmphysics, /twphysics  
/addcities, /rmcities, /twcities  
/addcountry, /rmcountry, /twcountry  
/addanimal, /rmanimal, /twanimal  
/addflowers, /rmflowers, /twflowers  
/addmathematics, /rmmathematics, /twmathematics  
/addprefix, /rmprefix, /caddprefix, /crmprefix, /twprefix, /listprefixes  
/addsuffix, /rmsuffix, /caddsuffix, /crmsuffix, /twsuffix, /listsuffixes  
/addnh, /rmnh, /twnh

Social & stats:
/stats – Show your personal stats  
/leaderboard – Show top players

Settings (Owner/Sudo):
/settimer – Set per-turn timer  
/setminlength – Set minimum word length for normal mode  
/setmaxplayers – Set maximum players per game

Admin & broadcast (Owner/Sudo):
/sudo, /unsudo, /listsudo  
/botban, /unbotban, /listbotbanned  
/permitgroup, /revokegroup, /listpermittedgroups  
/broadcast – Send a message to all permitted chats
""".strip()

def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)

def register(dp):
    dp.add_handler(CommandHandler("help", help_cmd))
