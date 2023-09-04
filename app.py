"""
    "DIES IST NICHT DAS ENDE"
    - Odradek 2022
"""

# Externe Module
import telebot
from telebot import types
from datetime import datetime

# Interne Module
from modules.bot.msgParse import process
from modules.bot.msgParse import handler

# Nicht öffentliche sichtbare Module/ Testmodule
from modules.bot.database import manusers
import credentials

err = "Kein Zugang möglich.\nDas kann zwei Gründe haben:\n-Deine eingegebenen Daten sind falsch\n-Die API ist überlastet.\nPrüfe die Daten und probiere es erneut!"

token = credentials.token()

bot = telebot.TeleBot(token, parse_mode="HTML")

@bot.message_handler(func=lambda m: True)
def handle_command(message):

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    userID = message.json["chat"]["id"]
    msg = str(message.text)

    log = current_time + " " + repr (message.json["chat"])+ " >> " + repr (message.text)

    if (msg == "/start"):
        # Der /start Befehl stellt eine Ausnahme dar und wird
        # exklusiv beim Start des Bots getriggert.

        markup = types.ReplyKeyboardMarkup(row_width = 2)
        
        nutzername = "🧑🏼‍🚀 Anmelden"
        hilfe      = "🛟 Hilfe"

        markup.add(nutzername, hilfe)
        
        text   = process.welcome()
        markup = markup

        manusers.add(userID)
        manusers.change(userID, "lastMsg", "/start")

        bot.send_message(userID, process.welcome(), reply_markup=markup)

        
    else:
        # Jeder weitere Input wird entsprechend mit dem Parser behandelt.
        handler.handle(userID, msg, bot)




bot.infinity_polling()