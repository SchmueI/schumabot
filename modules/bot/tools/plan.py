"""
"""

#Externe Module:
from datetime import datetime, timedelta

# Interne Module
from . import schedule, activity, meal, nextDates

def generate(userID, username, password, timeshift=0):
    
    datum = (
        datetime.today() + timedelta(days=timeshift)
    )

    weekday = datum.weekday()

    if (weekday == 0): weekday = "Montag"
    if (weekday == 1): weekday = "Dienstag"
    if (weekday == 2): weekday = "Mittwoch"
    if (weekday == 3): weekday = "Donnerstag"
    if (weekday == 4): weekday = "Freitag"
    if (weekday == 5): weekday = "Samstag"
    if (weekday == 6): weekday = "Sonntag"

    strDatum = datum.strftime("%d.%m.%Y")
    isoDatum = datum.strftime("%Y-%m-%d")
    
    # Fette Überschrift des Datums
    text = "<b>"+weekday+", "+strDatum+"</b>\n\n"

    # Lade Vertretungsplan
    element = schedule.get(userID, username, password, timeshift=0)
    if not element == "":
        text = text + "<u>Stunden- und Vertretungsplan</u>\n"
        text = text + element

        text = text + "\n"

    # Lade Informationen
    element = nextDates.get(userID, username, password, date=isoDatum)
    if not element == "":
        text = text + "<u>Info</u>\n"
        text = text + element
        
        text = text + "\n"

    # Lade Speiseplan
    weekstr = datum.strftime("%Y")+"-"+str(datum.isocalendar().week)
    element = meal.read(week = weekstr, weekday = weekday)
    if not element == "":
        text = text + "<u>Essen</u>\n"
        text = text + element

        text = text + "\n\n"

    # Lade Arbeitsgruppen
    element = activity.get(userID, username, password, date=isoDatum)
    if not element == "":
        text = text + "<u>Arbeitsgruppen</u>\n"
        text = text + element

    return text