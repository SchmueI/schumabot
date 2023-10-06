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
    text, markup = process.sendHelp(userID)

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

def changeUsernameData(userID, msg, bot):
    manusers.change (userID, "username", msg)
    manusers.change (userID, "lastMsg", "🧑🏼‍🚀 Zum Hauptmenü")

    usr = msg
    pwd = manusers.show(userID, "password")
    valid = approve.isValid(usr, pwd)

    if valid: manusers.change("verified", "true")
    else: manusers.change(userID, "verified", "false")

    text, markup = process.gotChange(userID, valid = valid)

    bot.send_message (
        userID,
        text,
        reply_markup = markup
    )

def changePasswordData(userID, msg, bot):
    manusers.change (userID, "password", msg)
    manusers.change (userID, "lastMsg", "🧑🏼‍🚀 Zum Hauptmenü")

    pwd = msg
    usr = manusers.show(userID, "username")
    valid = approve.isValid(usr, pwd)

    if valid: manusers.change(userID, "verified", "true")
    else: manusers.change(userID, "verified", "false")

    text, markup = process.gotChange(userID, valid = valid)

    bot.send_message (
        userID,
        text,
        reply_markup = markup
    )



def check (userID, msg, bot):
    lastMsg = manusers.show(userID, "lastMsg")
    
    if (lastMsg == "🧑🏼‍🚀 Anmelden"):                  appendUser      (userID, msg, bot)
    elif (lastMsg == "🔑 Passwort"):                appendPassword  (userID, msg, bot)
    elif (lastMsg == "👩🏽 Nutzername ändern"):       changeUsernameData(userID, msg, bot)
    elif (lastMsg == "🔑 Passwort ändern"):         changePasswordData(userID, msg, bot)
    else:
        unknownCommand(userID, msg, bot)

def mainMenue(userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)
    markup = process.mainMenue(userID)

    text = "🧑🏼‍🚀 Willkommen zurück."

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def sendPlan(userID, msg, timeshift, bot):
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text = plan.generate(bot, userID, username, password, timeshift=timeshift)

def sendVPlan(userID, msg, bot):
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text = process.getVPlan(userID, username, password)

    bot.send_message(
        userID,
        text
    )

def sendSPlan(userID, msg, bot):
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text = process.getSPlan(userID, username, password)

    bot.send_message(
        userID,
        text
    )

def sendAPlan(userID, msg, bot):
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text, markup = process.getAPlan(userID, username, password)

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def sendTPlan(userID, msg, bot):
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text, markup = process.getTPlan(userID, username, password)

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )


def iweOptions(userID, msg, bot):
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text, markup = process.triggerIWE(userID, username, password)

    bot.send_message(
        userID, 
        text,
        reply_markup = markup
    )

def iweChange(userID, msg, bot, state):
    manusers.change(userID, "lastMsg", msg)
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text, markup = process.sendIWE(userID, username, password, state)

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def showPlans(userID, msg, bot):
    text, markup = process.showPlans()

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def sendSettings(userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)
    username = manusers.show(userID, "username")
    password = manusers.show(userID, "password")

    text, markup = process.sendSettings(userID, username, password)

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def changeUsername(userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)

    text, markup = process.changeUsername()

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def changePassword(userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)

    text, markup = process.changePassword()

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def changeIWEauto(userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)

    text, markup = process.changeIWE(userID)

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def changeTagesNachricht(userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)

    text, markup = process.changeTagesNachricht(userID)

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )

def changeMainMen(userID, msg, bot):
    manusers.change(userID, "lastMsg", msg)

    text, markup = process.changeMainMen(userID)

    bot.send_message(
        userID,
        text,
        reply_markup = markup
    )
    

def handle(userID, msg, bot):
    
    # Dieses Modul sucht nach bekannten Nachrichtentypen
    # Wenn die Nachricht nicht dem erwarteten Typus entspricht,
    # wird eine Fehlermeldung ausgegeben.

    if not manusers.show(userID, "lastMsg") == "🧙🏻 Hauptmenü anpassen":
        if   (msg == "🛟 Hilfe")                    : sendHelp              (userID, msg, bot)
        elif (msg == "🧑🏼‍🚀 Anmelden")                 : register              (userID, msg, bot)
        
        elif (msg == "📅 Pläne")                    : showPlans             (userID, msg, bot)
        elif (msg == "☀️ Tagesplan")                : sendPlan              (userID, msg, 0, bot)
        elif (msg == "🌼 Nächster Plan")            : sendPlan              (userID, msg, 1, bot)
        elif (msg == "🥸 Vertretungsplan")          : sendVPlan             (userID, msg, bot)
        elif (msg == "🍽 Speiseplan")               : sendSPlan             (userID, msg, bot)
        elif (msg == "🏓 AG Plan")                  : sendAPlan             (userID, msg, bot)
        elif (msg == "📆 Terminplan")               : sendTPlan             (userID, msg, bot)
        elif (msg == "🏡 IWE")                      : iweOptions            (userID, msg, bot)

        elif (msg == "🌕 gesamtes IWE")             : iweChange             (userID, msg, bot, 1)
        elif (msg == "🌗 Fr - Sa")                  : iweChange             (userID, msg, bot, 2)
        elif (msg == "🌓 Sa - So")                  : iweChange             (userID, msg, bot, 3)
        elif (msg == "🌑 Abmelden")                 : iweChange             (userID, msg, bot, 0)

        elif (msg == "⚙️ Einstellungen")            : sendSettings          (userID, msg, bot)
        elif (msg == "👩🏽 Nutzername ändern")        : changeUsername        (userID, msg, bot)
        elif (msg == "🔑 Passwort ändern")          : changePassword        (userID, msg, bot)
        elif (msg == "🏡 IWE-Automatik ändern")     : changeIWEauto         (userID, msg, bot)
        elif (msg == "🌤 Tägliche Nachricht")       : changeTagesNachricht  (userID, msg, bot)
        elif (msg == "🧙🏻 Hauptmenü anpassen")       : changeMainMen         (userID, msg, bot)

        elif (msg in ["🧑🏼‍🚀 Zum Hauptmenü", "/main"]) : mainMenue             (userID, msg, bot)

        else:
            # Ab hier muss entschieden werden, ob eine Nachricht erwartet wird,
            # welche nicht den Befehlen entspricht.
            # Beispielsweise kann das der Fall sein, wenn eine Nutzereingabe erforderlich ist.
            check(userID, msg, bot)
    else:
        manusers.change(userID, "shortcut", msg)
        mainMenue (userID, msg, bot)
