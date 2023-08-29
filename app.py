"""
    "DIES IST NICHT DAS ENDE"
    - Odradek 2022
"""


import main.init
import main.login
import main.caldav
import main.schedules
import main.dashboard

import lsp.iwe

import credentials      # Dieses Modul ist nicht im Repository inkludiert.

err = "Kein Zugang möglich.\nDas kann zwei Gründe haben:\n-Deine eingegebenen Daten sind falsch\n-Die API ist überlastet.\nPrüfe die Daten und probiere es erneut!"

driver = init.init_driver(headless=False)

# Die Zugangsdaten werden von der Datenbank geladen.
# Wenn Sie diese API nutzen wollen, verwenden Sie Ihre eigenen Zugangsdaten.
username = credentials.username()
password = credentials.passwort()
#username = "Falsche Daten."

success, driver = login.login(driver, username=username, password=password)
if success:
    success, driver = dashboard.load(driver)
else:
    print ("DRIVER LOGIN\n" + err)

if success:
    iwe.register(driver)
else:
    print ("DRIVER DASHBOARD\n" + err)

init.close_driver(driver)
