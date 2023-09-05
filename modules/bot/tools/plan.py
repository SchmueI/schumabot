"""
"""

#Externe Module:
from datetime import datetime, timedelta

# Interne Module
from . import schedule

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

    datum = datum.strftime("%d.%m.%Y")
    
    text = "<b>"+weekday+", "+datum+"</b>\n\n"
    text = text + "<u>Stunden- und Vertretungsplan</u>\n"
    text = text + schedule.get(userID, username, password, timeshift=0)

    return text