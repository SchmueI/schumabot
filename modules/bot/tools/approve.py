"""
"""

from ...api.main import init
from ...api.main import login

def isValid(username, password):
    driver = init.init_driver(headless=True)
    
    success, driver = login.login(driver, username=username, password=password)

    init.close_driver(driver)

    return success