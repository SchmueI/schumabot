"""
"""

from ...api.main import init, login, dashboard, activities
from ..database import manusers

from datetime import datetime, timedelta

def get (userID, username, password, date="2023-01-01"):
    
    # Starte Selenium Driver, Nutze Login Daten.

    driver = init.init_driver(headless=True)

    success, driver = login.login(driver, username=username, password=password)

    # Wenn der Login scheitert, sollte das in der Datenbank vermerkt werden.
    if success: manusers.change (userID, "approved", "true")
    else: manusers.change (userID, "approved", "false")

    success, driver = dashboard.load(driver)

    # Sortiere Daten, sodass sie eine Nachricht ergeben.
    table = []
    text = "Es ist ein unbekannter Fehler aufgetreten.\nProbiere es erneut oder kontaktiere @schmuel."
    if success:
        table = activities.get(driver, date = date)

        text = ""
        for activity in table:
            text = text + "• " + activity + "\n"
        if text == "• \n": text = ""
    
    init.close_driver(driver)
    
    return text

def get_week(userID, username, password):

    # Starte Selenium Driver, Nutze Login Daten.

    driver = init.init_driver(headless=True)

    success, driver = login.login(driver, username=username, password=password)

    # Wenn der Login scheitert, sollte das in der Datenbank vermerkt werden
    if success: manusers.change(userID, "approved", "true")
    else: manusers.change (userID, "approved", "false")

    success, driver = dashboard.load(driver)

    text = "Es ist ein unbekannter Fehler aufgetreten.\nProbiere es erneut oder kontaktiere @schmuel"

    # Sortiere Daten, sodass sie eine Nachricht ergeben:
    table = []
    if success:

        # Konvertiere übergebenes Datum in auslesbares Format:
        DT = datetime.today()
        text = "<u>Kommende Arbeitsgruppen</u>\n"
        for i in range(7):
            if DT.weekday() == 0: weekday = "Montag"
            if DT.weekday() == 1: weekday = "Dienstag"
            if DT.weekday() == 2: weekday = "Mittwoch"
            if DT.weekday() == 3: weekday = "Donnerstag"
            if DT.weekday() == 4: weekday = "Freitag"
            if DT.weekday() == 5: weekday = "Samstag"
            if DT.weekday() == 6: weekday = "Sonntag"

            sttringDay = DT.strftime("%d.%m.%Y")
            date = DT.strftime("%Y-%m-%d")
            text = text + "\n<b>"+weekday + ", "+sttringDay+"</b>\n"
            table = activities.get(driver, date = date)

            for activity in table:
                text = text + "• " + activity + "\n"
            
            DT = DT + timedelta(days=1)
    return text
