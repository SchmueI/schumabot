"""
"""

from ...api.main import init, login, schedules
from ..database import manusers

from datetime import datetime, timedelta

def get(userID, username, password, timeshift=0):

    # Ermittle den Tag, dessen Plan abgerufen werden soll.
    weekday = datetime.today() + timedelta(days=timeshift)
    weekday = weekday.weekday()

    # Starte Selenium Driver, Nutze Login Daten.
    driver = init.init_driver(headless=True)

    success, driver = login.login(driver, username=username, password=password)

    # Wenn der Login scheitert, sollte das in der Datenbank vermerkt werden.
    if success: manusers.change(userID, "approved", "true")
    else: manusers.change(userID, "approved", "false")

    # Sortiere Daten, sodass sie eine Nachricht ergeben.
    table = []
    if success:
        table = schedules.getPlan(weekday, driver)
        
        text = ""
        i = 1
        for lesson in table:
            if not i > 10:
                text = text + "• " + str(i) + ". " + lesson + "\n"
            i = i+1
    else: text = "Error: Keine Verbindung möglich"
    init.close_driver(driver)
    return text