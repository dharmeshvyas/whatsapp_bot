import json
import messageData


def addAnnouncement(message):
    messageData.EditMessage(5, "Replay", message)


def isAdmin(contact):
    if contact == "+916353785601":
        return True
    else:
        return False
