import json
from selenium.webdriver.common.keys import Keys


def MessageLoad(typeofdata="user"):


    if typeofdata=="admin":
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


def AddMessages(message, replay):
    lastid = None
    with open("./Data/response.json", "r") as readfile:
        data = json.load(readfile)
        lastid = len(data) + 1
    with open("./Data/response.json", "w") as addfile:
        entry = {"id": lastid, "message": message, "Replay": replay}
        print("Inserted data :", entry)
        data.append(entry)
        json.dump(data, addfile, indent=4)

data = open("./Data/commandlist.txt", "r")
commandlist = data.read()

