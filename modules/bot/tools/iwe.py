"""
"""

from ...api.main import init, login, dashboard
from ...api.lsp  import iwe
from ..database  import manusers

def loadState(userID, username, password):

    # Starte Selenium Driver, Nutze Login Daten.
    driver = init.init_driver(headless=True)

    success, driver = login.login(driver, username=username, password=password)
    success, driver = dashboard.load(driver)

    # Wenn der Login scheitert, sollte das in der Datenbank vermerkt werden.
    if success: manusers.change (userID, "approved", "true")
    else:       manusers.change (userID, "approved", "false")

    # Ermittle Status
    success, state, driver = iwe.status(driver)

    init.close_driver(driver)
    
    return state

def sendState(userID, username, password, state):
    
    # Starte Selenium Driver, Nutze Login Daten.
    driver = init.init_driver(headless=True)

    success, driver = login.login(driver, username=username, password=password)
    success, driver = dashboard.load(driver)

    # Wenn der Login scheitert, sollte das in der Datenbank vermerkt werden.
    if success: manusers.change (userID, "approved", "true")
    else:       manusers.change (userID, "approved", "false")

    # Sende Status
    success, driver = iwe.register(driver, state)

    init.close_driver(driver)

    return success
    