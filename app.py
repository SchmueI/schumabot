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
    reply = bot.send_message(message.json["chat"]["id"], "🧑🏼‍🚀 Deine Anfrage wird bearbeitet.\n🌱 Bitte hab etwas Geduld.\n🐌 Derzeit bin ich lahm.")
    messages.append([message, reply])


def run_commands():
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

def updateQueue():
    
    akt = 1
    render = " |"

    while True:

        if akt == 9: akt = 1

        if akt == 1: render = " |"
        if akt == 2: render = " /"
        if akt == 3: render = " –"
        if akt == 4: render = " \\"
        if akt == 5: render = " |"
        if akt == 6: render = " /"
        if akt == 7: render = " -"
        if akt == 8: render = " \\"

        akt += 1

        pos = 1
        for request in list(messages):
            reply = request[1]

            txt = """
🧑🏼‍🚀 Deine Anfrage wird bearbeitet.
🌱 Bitte hab etwas Geduld.
🐌 Derzeit bin ich lahm.

🐍 <code>Warteschlange: """
            txt = txt + str(pos) + render+"</code>"
            try:
                bot.edit_message_text(txt, reply.chat.id, reply.message_id)
            except:
                txt = txt
            pos = pos+1
        sleep(1)

def iterate():
    while True:
        sleep(1)
        run_commands()

_thread.start_new_thread(iterate, ())
_thread.start_new_thread(updateQueue, ())

bot.infinity_polling()