"""
"""

import json

def read(week = "2023-01", weekday="Montag"):

    outp = ""
    with open ("meal.json", "r") as file:
        DATA = json.load(file)
        if (week in DATA):
            WEEK = DATA[week]

            if (weekday in WEEK):
                MENUE = WEEK[weekday]

                men1 = MENUE["1"]
                men2 = MENUE["2"]
                men3 = MENUE["V"]
                dess = MENUE["D"]

                # Prüfe, ob es ein Tagesmenü gibt
                # oder ob Einzelmenüs hinterlegt sind.
                    
                if (
                    men1 == "" and
                    men2 == "" and
                    men3 == "" and
                    dess == "" 
                ):
                    if (not MENUE["M"] == ""):
                        menu = MENUE["M"]
                        menu = menu.split("--")

                        for entity in menu:
                            outp = outp+"• "+entity+"\n"

                    else: output="• kein Essensplan hinterlegt"
                else:
                    outp = outp + "• 1: " + men1 + "\n"
                    outp = outp + "• 2: " + men2 + "\n"
                    outp = outp + "• V: " + men3 + "\n"
                    outp = outp + "• D: " + dess

            else:
                # Wochentag nicht gefunden
                outp = "• Fehler: Wochentag wurde nicht gefunden.\nDiese Nachricht sollte hoffentlich n i e m a l s angezeigt werden..."

        else:
            # Woche nicht gefunden
            outp="• kein Essensplan hinterlegt"

    return outp
    
