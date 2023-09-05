"""
"""

# Nicht-öffentliche Module
from ..database import manusers

# Interne Module
from . import process

from ..tools import approve
from ..tools import schedule
from ..tools import plan

# Externe Module
from datetime import datetime

def register (userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)
    text, markup = process.register()

    bot.send_message (
        userID,
        text,
        reply_markup = markup
    )

def sendHelp (userID, msg, bot):
    text, markup = process.sendHelp()

    bot.send_message (
        userID,
        text,
        reply_markup = markup
    )

def unknownCommand(userID, msg, bot):
    msg = """
Dieses Kommando kenne ich nicht.
"""
    bot.send_message(userID, msg)

def appendUser(userID, msg, bot):
    manusers.change(userID, "username", msg)
    manusers.change(userID, "lastMsg", "🔑 Passwort")

    text, markup = process.gotUser()

    bot.send_message (
        userID,
        text,
        reply_markup = markup
    )

def sendCurrentPlan(userID, msg, bot):
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text = plan.generate(userID, username, password, timeshift=0)

    markup = process.mainMenue(userID)

    bot.send_message (
        userID,
        text,
        reply_markup = markup
    )
    
    

def appendPassword(userID, msg, bot):
    manusers.change(userID, "password", msg)
    manusers.change(userID, "lastMsg", "🧑🏼‍🚀 Zum Hauptmenü")

    password = msg
    username = manusers.show(userID, "username")
    valid = approve.isValid(username, password)
    
    if valid: manusers.change(userID, "verified", "true")
    else: manusers.change(userID, "verified", "false")

    text, markup = process.gotPassword(userID, valid = valid)

    bot.send_message (
        userID,
        text,
        reply_markup = markup
    )


def check (userID, msg, bot):
    lastMsg = manusers.show(userID, "lastMsg")
    
    if (lastMsg == "🧑🏼‍🚀 Anmelden"):      appendUser      (userID, msg, bot)
    elif (lastMsg == "🔑 Passwort"):    appendPassword  (userID, msg, bot)
    else:
        unknownCommand(userID, msg, bot)


def handle(userID, msg, bot):
    
    # Dieses Modul sucht nach bekannten Nachrichtentypen
    # Wenn die Nachricht nicht dem erwarteten Typus entspricht,
    # wird eine Fehlermeldung ausgegeben.

    if   (msg == "🛟 Hilfe")    : sendHelp          (userID, msg, bot)
    elif (msg == "🧑🏼‍🚀 Anmelden") : register          (userID, msg, bot)
    elif (msg == "☀️ Tagesplan"): sendCurrentPlan   (userID, msg, bot)
    else:
        # Ab hier muss entschieden werden, ob eine Nachricht erwartet wird,
        # welche nicht den Befehlen entspricht.
        # Beispielsweise kann das der Fall sein, wenn eine Nutzereingabe erforderlich ist.
        check(userID, msg, bot)