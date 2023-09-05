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
    if success:
        table = activities.get(driver, date = date)

        text = ""
        for activity in table:
            text = text + "• " + activity + "\n"
    
    init.close_driver(driver)
    
    return text
        