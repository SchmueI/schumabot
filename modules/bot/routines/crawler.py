"""
"""

from ..database import manusers
from ..tools import iwe
from ..tools import plan

def regIWE(bot):
    DATA = manusers.get_DATA()
    users = []
    for i in DATA: 
        users.append(i)
    
    for i in range (len(users)):
        if DATA[users[i-1]]["autoIWE"] == "true":
            username = DATA[users[i-1]]["username"]
            password = DATA[users[i-1]]["password"]
            
            success = iwe.sendState(users[i-1], username, password, 1)
            
            if success: bot.send_message(users[i-1], "🌟 Ich habe dich zum IWE angemeldet!")
            else: bot.send_message(users[i-1], "🔥 Ich wollte dich zum IWE anmelden \n🥀Aber es hat nicht geklappt...")
        
        else:
            print ("Nutzer wird übersprungen")

def sendRoutine(bot):

    print ("Beginne mit dem Versenden der Tagesnachrichten")

    DATA = manusers.get_DATA()
    users = []
    for i in DATA: 
        users.append(i)
    
    for i in range (len(users)):
        ratio = i/len(users) * 100
        print ( str(i) + " / " + str(len(users)) + "  " + str(ratio)+"%")
        
        if DATA[users[i-1]]["daily"] == "true":
            username = DATA[users[i-1]]["username"]
            password = DATA[users[i-1]]["password"]

            print (username)
            print (password)
            
            text = plan.generate(bot, users[i-1], username, password, timeshift=1, showProcess = False)

            bot.send_message(users[i-1], text)
