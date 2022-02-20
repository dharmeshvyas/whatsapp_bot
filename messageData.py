import json
from selenium.webdriver.common.keys import Keys

def MessageLoad(typeofdata="user"):
    if typeofdata == "admin":
        f = open("./Data/adminresponse.json")
        bigdata = json.load(f)
        f.close()
        return bigdata
    else:
        f = open("./Data/response.json")
        bigdata = json.load(f)
        f.close()
        return bigdata

def EditMessage(index, key, messsage, data=None):
    with open("./Data/response.json", "r") as readfile:
        data = json.load(readfile)

    data[index][key] = messsage + "\n"
    with open("./Data/response.json", "w") as updatefile:
        json.dump(data, updatefile)

    print(messsage)

def ALluser():
    newline = (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)
    message = f"╔══════▓▓ LIST OF Users▓▓══════╗{newline}||{newline}"
    with open("./Data/users.json","r") as userfile:
        users = json.load(userfile)
    for user in users:
        message += f"||{newline}╠》 {user['contact']}{newline}"
    return message

def AddMessages(message):
    MandR = message.split("-")
    print(MandR)
    lastid = None
    with open("./Data/response.json", "r") as readfile:
        data = json.load(readfile)
        lastid = len(data) + 1
    with open("./Data/response.json", "w") as addfile:
        entry = {"id": lastid, "message": MandR[0], "Replay": MandR[1]}
        print("Inserted data :", entry)
        data.append(entry)
        json.dump(data, addfile, indent=4)

def getCommandlist(usertype="user"):
    newline = (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)
    message = f"▁▂▄▅▆▇█ WELCOME TO DV'S BOT █▇▆▅▄▂▁{newline}╔══════▓▓ LIST OF COMMANDS▓▓══════╗{newline}||{newline}"

    usercommand = MessageLoad()
    if usertype=="admin":
        for command in usercommand:
            message += f"||{newline}╠》 {command['message']}{newline}"
        admincommnads = MessageLoad("admin")
        for command in admincommnads:
            message += f"||{newline}╠》 {command['message']}{newline}"
    else:
        for command in usercommand:
            message += f"||{newline}╠》 {command['message']}{newline}"

    return message

