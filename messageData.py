import json


def MessageLoad():
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
