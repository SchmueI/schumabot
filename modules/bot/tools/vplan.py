"""
"""

from ...api.main import init, login, schedules
from ..database import manusers

def get (userID, username, password):

    # Starte Selenium Driver, Nutze Login Daten.
    driver = init.init_driver(headless=True)
    success, driver = login.login(driver, username=username, password=password)
    
    # Wenn der Login scheitert, sollte das in der Datenbank vermerkt werden
    if success: manusers.change (userID, "approved", "true")
    else: manusers.change (userID, "approved", "false")

    # Sammle Daten
    table = []
    if success:
        table = schedules.getPlan(0, driver, ALL=True)

        text = ""
        

        d = 0
        for day in table:
            exchange = ""
            i = 0
            for lesson in day:
                if not i > 10:
                    if ( "→" in lesson):
                        exchange = exchange + "• " + str(i) + ". " + lesson + "\n"
                i = i+1
            if not exchange == "":

                if d == 0: weekday = "Montag"
                if d == 1: weekday = "Dienstag"
                if d == 2: weekday = "Mittwoch"
                if d == 3: weekday = "Donnerstag"
                if d == 4: weekday = "Freitag"

                text = text + "\n<u>"+weekday+"</u>\n"+exchange
            d = d+1

        
    else: text = "Error: Keine Verbindung möglich"
    init.close_driver(driver)

    return text