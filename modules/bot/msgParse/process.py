"""
"""

# Externe Module
import importlib
from telebot import types
from datetime import datetime

# Nicht öffentliche Module
from ..database import manusers

# Interne Module
from ..tools import iwe
from ..tools import vplan
from ..tools import meal
from ..tools import activity
from ..tools import nextDates

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
    #bus             = types.KeyboardButton("🚌 Schulbus")
    settings        = types.KeyboardButton("⚙️ Einstellungen")

    markup.add(fav, pläne, lehrerdaten, IWE, settings)

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

    return msg, markup

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

def triggerIWE(userID, username, password):
    
    state = iwe.loadState(userID, username, password)

    if state == "Nicht angemeldet"          : state = "🌑 "+state
    if state == "Gesamtes IWE"              : state = "🌕 "+state
    if state == "Nur Freitag bis Samstag"   : state = "🌗 "+state
    if state == "Nur Samstag bis Sonntag"   : state = "🌓 "+state

    msg = "🏡 <b>IWE-Anmeldung</b>\n\n🧑🏼‍🚀 Aktueller Anmeldestand: \n"+state

    markup = types.ReplyKeyboardMarkup(row_width = 2)

    frso = "🌕 gesamtes IWE"
    frsa = "🌗 Fr - Sa"
    saso = "🌓 Sa - So"
    noth = "🌑 Abmelden"
    main = "🧑🏼‍🚀 Zum Hauptmenü"

    markup.add(frso)
    markup.add(frsa, saso)
    markup.add(noth)
    markup.add(main)

    return msg, markup

def sendIWE(userID, username, password, state):

    success = iwe.sendState(userID, username, password, state)
    markup  = mainMenue(userID)

    if success:
        msg = "💫 Deine Einstellung wurde übernommen"
    else:
        msg = "🤺 Das hat nicht geklappt\n🌫 Vielleicht gibt es kein IWE\n🌤 Probiere es gern später erneut!"

    return msg, markup

def showPlans():
    msg = "📆 Folgende Pläne kann ich dir zeigen:"

    markup = types.ReplyKeyboardMarkup(row_width = 2)
    
    tagesp = "☀️ Tagesplan"
    morpla = "🌼 Nächster Plan"
    verpla = "🥸 Vertretungsplan"
    speipl = "🍽 Speiseplan"
    agplan = "🏓 AG Plan"
    terpla = "📆 Terminplan"
    mainme = "🧑🏼‍🚀 Zum Hauptmenü"

    markup.add (tagesp, morpla, verpla, speipl, agplan, terpla, mainme)

    return msg, markup

def getVPlan(userID, username, password):
    DATA = vplan.get(userID, username, password)
    if DATA == "": DATA = "• Keine Vertretung eingeplant"
    
    msg = "<b>Vertretungsplan</b>\n"
    msg = msg + DATA

    return msg

def getSPlan(userID, username, password):
    date = datetime.today()
    day = datetime.today().weekday()
    collect = []
    
    for i in range(7):
        if i == 0: daystr = "Montag"
        if i == 1: daystr = "Dienstag"
        if i == 2: daystr = "Mittwoch"
        if i == 3: daystr = "Donnerstag"
        if i == 4: daystr = "Freitag"
        if i == 5: daystr = "Samstag"
        if i == 6: daystr = "Sonntag"
        if day <= i:
            collect.append(daystr)
    
    msg = "<b>Speiseplan</b>\n"
    
    week = date.strftime("%Y")+"-"+str(date.isocalendar().week)
    for i in collect:
        element = meal.read(week=week, weekday=i)
        msg = msg + "\n<u>"+i+"</u> \n"
        msg = msg + element + "\n"

    return msg

def getAPlan(userID, username, password):
    return activity.get_week(userID, username, password), mainMenue(userID)
    

def getTPlan(userID, username, password):
    return nextDates.get_week(userID, username, password), mainMenue(userID)

def settings():
    markup = types.ReplyKeyboardMarkup(row_width = 2)

    neuerNutzer = "👩🏽 Nutzername ändern"
    neuesPasswort = "🔑 Passwort ändern"
    IWE = "🏡 IWE-Automatik ändern"
    daily = "🌤 Tägliche Nachricht"
    Shortcut = "🧙🏻 Hauptmenü anpassen"
    mainme = "🧑🏼‍🚀 Zum Hauptmenü"

    markup.add(neuerNutzer, neuesPasswort, IWE, daily, Shortcut, mainme)
    
    return markup

def sendSettings(userID, username, password):

    fav = manusers.show(userID, "shortcut")
    username = username
    password = password
    autoIWE = manusers.show(userID, "autoIWE")
    if autoIWE == "true": autoIWE = "An"
    else: autoIWE = "Aus"
    DAILY = manusers.show(userID, "daily")
    if DAILY == "true": DAILY = "An"
    else: DAILY = "Aus"

    text = """
<b>Deine Daten:</b>
<code>
Nutzername:         </code><tg-spoiler>"""+username+"""</tg-spoiler><code>
Passwort:           </code><tg-spoiler>"""+password+"""</tg-spoiler><code>
IWE-Automatik:      </code>"""+autoIWE+"""<code>
Tägliche Nachricht: </code>"""+DAILY+"""<code>
Hauptmenü-Shortcut: </code>"""+fav+"""<code>
</code>
"""

    return text, settings()

def changeUsername():
    
    text = """
🥸 Sende mir deine neue E-Mail Adresse!
"""
    markup = none()

    return text, markup

def changePassword():
    
    text = """
🔑 Sende mir dein neues Passwort!
"""
    markup = none()

    return text, markup

def gotChange(userID, valid):
    if valid:
        text="""
🧑🏼‍🚀 Wunderbar.
💫 Ich habe deine Daten aktualisiert.
🌟 Du kannst den Bot nun normal weiterbenutzen.
"""
        markup = mainMenue(userID)
    else:
        text = """
🧑🏼‍🚀 Ich sach ma so:
💫 Deine Daten wurden aktualisiert.
☄️ Allerdings passen Nutzername und Passwort nun nicht mehr zusammen....
🌚 Bitte passe deine Daten an.
"""

        markup = types.ReplyKeyboardMarkup(row_width = 2)

        neuerNutzer = "👩🏽 Nutzername ändern"
        neuesPasswort = "🔑 Passwort ändern"

        markup.add(neuerNutzer, neuesPasswort)

    return text, markup

def changeIWE(userID):
    if manusers.show(userID, "autoIWE") == "true":
        manusers.change(userID, "autoIWE", "false")
        text = """
🧑🏼‍🚀 Die automatische IWE-Anmeldung wurde deaktiviert.
💫 Ab jetzt musst du eigenständig die Anmeldung vornehmen.
"""
    else:
        manusers.change(userID, "autoIWE", "true")
        text = """
🧑🏼‍🚀 Die automatische IWE-Anmeldung wurde aktiviert.
💫 Ab jetzt wirst du automatisch zu IWE angemeldet.

🪐 Ich werde dich immer informieren, wenn ich dich angemeldet habe
💥 Beachte, dass du allein die Verantwortung über die IWE-Anmeldung trägst.
"""
    return text, settings()

def changeTagesNachricht(userID):
    if manusers.show(userID, "daily") == "true":
        manusers.change(userID, "daily", "false")
        text = """
🧑🏼‍🚀 Ich bin schon still.
💫 Ab jetzt kriegst du keine täglichen Nachrichten mehr.
"""
    else:
        manusers.change(userID, "daily", "true")
        text = """
🧑🏼‍🚀 S T A T U S B E R I C H T
💫 Ab jetzt kriegst du Tagesmeldungen.
"""

    return text, settings()


def changeMainMen(userID):
    text = """
🧑🏼‍🚀 Whuuiiii
🌾 Du kannst das Hauptmenü anpassen
🌱 Wähle, welcher Eintrag oben links angeheftet werden soll!
"""

    markup = types.ReplyKeyboardMarkup(row_width = 2)

    a = "📅 Pläne"
    b = "☀️ Tagesplan"
    c = "🌼 Nächster Plan"
    d = "🥸 Vertretungsplan"
    e = "🍽 Speiseplan"
    f = "🏓 AG Plan"
    g = "📆 Terminplan"
    h = "🏡 IWE"
    i = "🌕 gesamtes IWE"
    j = "🌗 Fr - Sa"
    k = "🌓 Sa - So"
    l = "🌑 Abmelden"
    m = "⚙️ Einstellungen"
    n = "👩🏽 Nutzername ändern"
    o = "🔑 Passwort ändern"
    p = "🏡 IWE-Automatik ändern"
    q = "🌤 Tägliche Nachricht"
    r = "🧙🏻 Hauptmenü anpassen"

    markup.add (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r)

    return text, markup

