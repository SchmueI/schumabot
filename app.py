"""
    "DIES IST NICHT DAS ENDE"
    - Odradek 2022
"""

# Externe Module
import telebot
from telebot import types
from datetime import datetime
from time import sleep
import os
import _thread

# Interne Module
from modules.bot.msgParse import process
from modules.bot.msgParse import handler

# Nicht öffentliche sichtbare Module/ Testmodule
from modules.bot.database import manusers
import credentials

err = "Kein Zugang möglich.\nDas kann zwei Gründe haben:\n-Deine eingegebenen Daten sind falsch\n-Die API ist überlastet.\nPrüfe die Daten und probiere es erneut!"

token = credentials.token()

bot = telebot.TeleBot(token, parse_mode="HTML")

messages = []

@bot.message_handler(func=lambda m: True)
def handle_command(message):

    reply = bot.send_message(message.json["chat"]["id"], "🧑🏼‍🚀 Deine Anfrage wird bearbeitet.\n🌱 Bitte hab etwas geduld.\n🐌 Derzeit bin ich lahm.")
    messages.append([message, reply])


def run_commands():
    print("JA; HIER GEHT ES LOS")
    for request in list(messages):
        message = request[0]
        reply = request[1]
        
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

        elif (msg == "exit"):
            if (userID in credentials.adminID()):
                bot.send_message(155667852, "Der Bot wird beendet.", parse_mode="HTML")
                os.system('kill %d' % os.getpid())
            
        else:
            # Jeder weitere Input wird entsprechend mit dem Parser behandelt.
            handler.handle(userID, msg, bot)
        messages.remove(request)

        bot.delete_message(reply.chat.id, reply.message_id)


def iterate():
    while True:
        sleep(1)
        run_commands()
        print ("STARTE ABRUF DER BEFEHLE")

_thread.start_new_thread(iterate, ())

bot.infinity_polling()
