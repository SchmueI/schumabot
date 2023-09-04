"""
"""

# Externe Module
import importlib
from telebot import types

# Nicht öffentliche Module
from ..database import manusers

no_markup = types.ReplyKeyboardRemove(selective=False)

def none():
    return no_markup

def mainMenue(userID):
    
    markup = types.ReplyKeyboardMarkup(row_width=2)

    fav             = manusers.show(userID, "shortcut")
    
    fav             = types.KeyboardButton(fav)
    pläne           = types.KeyboardButton("📅 Pläne")
    lehrerdaten     = types.KeyboardButton("🧑🏼‍🏫 Lehrerdaten")
    IWE             = types.KeyboardButton("🏡 IWE")
    bus             = types.KeyboardButton("🚌 Schulbus")
    settings        = types.KeyboardButton("⚙️ Einstellungen")

    markup.add(fav, pläne, lehrerdaten, IWE, bus, settings)

    return markup


def welcome():
    msg = """
🤖 Willkommen beim SchuMa Bot.
🏫 Über 2.400 Schulen nutzen den Schulmanager.

🚀 Ich möchte es dir etwas einfacher machen.
🚥 Um zu beginnen, nutze die Schaltflächen und gib deine Zugangsdaten zum Schulmanager an.

🧑🏼‍⚖️ Wichtig! Mit deiner Anmeldung stimmst du den AGB und der Datenschutzerklärung zu.
🧙🏻 In diesen Dokumenten findest du alles darüber, wie du den Bot nutzen kannst und wie wir mit deinen Daten umgehen.
Es ist wichtig, dass du sie dir sorgfältig durchliest und bei Fragen Kontakt mit uns aufnimmst.

AGB: https://schumabot.schmuel.net/agb
Datenschutz: https://schumabot.schmuel.net/daschu

🧑🏼‍🚀 Startklar? Dann nutze jetzt den Anmeldebutton!
"""
    return msg


def sendHelp(userID):

    msg = """
Dies ist eine Hilfenachricht.
"""

    if manusers.show(userID, "lastMsg") == "/start":
        markup = types.ReplyKeyboardMarkup(row_width = 2)

        nutzername = "🧑🏼‍🚀 Anmelden"
        hilfe      = "🛟 Hilfe"

        markup.add(nutzername, hilfe)
    else:
        markup = mainMenue(userID)

def register():
    msg = """
🧑🏼‍🚀 Es kann losgehen!
👤 Als erstes brauche ich deine E-Mail Adresse
📨 Nutze die Adresse, die du beim Schulmanager verwendest.
"""
    markup = none()

    return msg, markup

def gotUser():
    msg = """
🧑🏼‍🚀 Wunderbar!
🔑 Als nächstes brauche ich dein Passwort.
🚪 Verwende dein Passwort von Schulmanager dafür.
"""

    markup = none()

    return msg, markup

def gotPassword(userID, valid=False):
    if valid:
        msg = """
🧑🏼‍🚀 Hussa!
🎩 Du hast dich erfolgreich mit dem Schulmanager verbunden.
"""
        markup = mainMenue(userID)

        return msg, markup
    else:
        msg = """
🧑🏼‍🚀 Ohje...
🪶 Das hat nicht geklappt!
🦥 Entweder ist der Server überlastet,
❄️ Oder deine Zugangsdaten falsch.

⚡️ Verwende deine Daten von Schulmanager
🌈 Und probiere es erneut!
"""
        markup = types.ReplyKeyboardMarkup(row_width = 2)

        nutzername = "🧑🏼‍🚀 Anmelden"
        hilfe      = "🛟 Hilfe"

        markup.add(nutzername, hilfe)

        return msg, markup