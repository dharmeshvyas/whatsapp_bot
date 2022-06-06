import json
import messageData
from termcolor import colored
import datetime
import art
from colorama import Fore


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

def printBio():
    print(art.text2art("WhatsApp Bot"))
    print(Fore.CYAN + "\nCreated By:" + Fore.RESET + " Dharmesh vyas\n")
    print(Fore.YELLOW + "GitHub: " + Fore.RESET + "   dharmeshvyas")
    print(Fore.YELLOW + "Instagram:" + Fore.RESET + " @dharmeshvyas.dv")

def PrintDetails(message,type):
    if type == 'INFO':
        print('[' + colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan') + '][' + colored('INFO',
                                                                                                   'green') + '] ' + message)
    elif type == 'WARNING':
        print('[' + colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan') + '][' + colored('WARNING',
                                                                                                   'yellow') + '] ' + message)
    elif type == 'MESSAGE':
        print('[' + colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan') + '][' + colored('MESSAGE',
                                                                                                    'green') + '] ' + message)
    elif type == 'USER':
        print('[' + colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan') + '][' + colored('USER',
                                                                                                   'blue') + '] ' + message)
    elif type == 'ERROR':
        print('[' + colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan') + '][' + colored('ERROR',
                                                                                                   'red') + '] ' + message)

