import json
import messageData


def addAnnouncement(message):
    messageData.EditMessage(5, "Replay", message)


def isAdmin(contact):
    if contact == "+916353785601" or contact == "Me":
        return True
    else:
        return False

def isUser(contact):
    f = open("./Data/users.json")
    users = json.load(f)
    f.close()
    for user in users:
        if user['contact'] == contact:
            return True
    else:
        return False

def addUser(contact):
    lastid = None
    with open("./Data/users.json", "r") as readfile:
        data = json.load(readfile)
        lastid = len(data) + 1

    with open("./Data/users.json", "w") as addfile:
        entry = {"id": lastid, "contact": contact}
        print("Inserted data :", entry)
        data.append(entry)
        json.dump(data, addfile, indent=4)
