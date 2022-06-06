from colorama import Fore
from MyQR import myqr as qr
import ascii_magic

qr.run("Hello there check qr code",save_name = 'qrcode.png')
output = ascii_magic.from_image_file("qrcode.png",columns=50,char= "▓",width_ratio=2.5,back=ascii_magic.Back.BLACK,mode = ascii_magic.Modes.TERMINAL)
print(output)
#▅

import platform,os
#TEXT INTO FONT DESING
import art
#FOR CONSOLE COLORFUL TEXT
def printBio():
    print(art.text2art("WhatsApp Bot"))
    print(Fore.CYAN + "\nCreated By:" + Fore.RESET + " Dharmesh vyas\n")
    print(Fore.YELLOW + "GitHub: " + Fore.RESET + "   dharmeshvyas")
    print(Fore.YELLOW + "Instagram:" + Fore.RESET + " @dharmeshvyas.dv")
