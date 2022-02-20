import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import re, pyperclip
from unicodedata import normalize
import messageData
import features as feat


class WhatsappBot:
    username =None
    def __init__(self):
        opt = Options()
        opt.headless = False
        opt.add_argument("--no-sandbox")
        opt.add_argument("--user-data-dir=/home/dv/chromedata/user-1")
        opt.add_argument("--disable-dev-shm-usage")
        service = Service("./driver/chromedriver")
        # service = Service("./driver/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=opt)
        self.Waiter = WebDriverWait(self.driver, 10)

    def search_chat(self):
        # feat.PrintDetails("searching chats", 'INFO')

        if len(self.Waiter.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "zaKsw")),
                                 "chats not found")) == 0:
            # feat.PrintDetails("chat opened", 'INFO')

            message = self.identifying_message()
            if message is not None:
                return True

        chats = self.driver.find_elements(By.CLASS_NAME, "_3m_Xw")
        for chat in chats:
            # feat.PrintDetails("detecting unread messages", 'INFO')

            unread_chats = chat.find_elements(By.CLASS_NAME, "cfzgl7ar")

            if len(unread_chats) == 0:
                # feat.PrintDetails("chat answered", 'INFO')
                continue

            element_name = chat.find_elements(By.CLASS_NAME, 'zoWT4')
            WhatsappBot.username = element_name[0].text.replace(" ", "")
            feat.PrintDetails(WhatsappBot.username, 'USER')
            if feat.isUser(WhatsappBot.username):
                pass
            else:
                feat.addUser(WhatsappBot.username)
            chat.click()
            return True
        return False

    def identifying_message(self, element=1):

        element_box_message = self.driver.find_elements(By.CLASS_NAME, "Nm1g1")
        position = len(element_box_message) - element

        color = element_box_message[position].value_of_css_property("background-color")

        if color == "rgba(220, 248, 198, 1)" or color == "rgba(5, 97, 98, 1)":
            # feat.PrintDetails("chat identified", "INFO")
            return

        element_message = element_box_message[position].find_elements(By.CLASS_NAME, "_1Gy50 ")
        message = element_message[0].text.lower()
        if element==1:
            feat.PrintDetails(message, "MESSAGE")
        return message

    def normalizer(self, message: str):
        message = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
            normalize("NFD", message), 0, re.I
        )

        return normalize("NFD", message)

    def prepared_response(self, message: str):

        # feat.PrintDetails("find response", "INFO")
        data = messageData.MessageLoad()

        # for user
        if not feat.isAdmin(WhatsappBot.username):
            for index in data:
                if message.__contains__(index['message']):
                    response = index['Replay']
                    return response + "\n"
                elif message.__contains__("list"):
                    response = messageData.getCommandlist()
                    return response+"\n"
            else:
                response = "invalid message do you want see command list(yes/no)"
                if message.__contains__('yes'):
                    response = messageData.getCommandlist()
                    return response + "\n"
                elif message.__contains__('no'):
                    return "AS you Wish\n"
                else:
                    pass
                return response + "\n"

        # FOR ADMIN
        else:
            for index in data:
                if message.__contains__(index['message']):
                    response = index['Replay']
                    return response + "\n"
                elif message.__contains__("list"):
                    response = messageData.getCommandlist("admin")
                    return response+"\n"
            else:
                admindata = messageData.MessageLoad("admin")
                for index in admindata:
                    if message.__contains__(index['message']):
                        response = index['response']
                        if message.__contains__('alluser'):
                            response = messageData.ALluser()
                        return response + "\n"
                    elif self.identifying_message(3) == "add message":
                        messageData.AddMessages(message)
                        return "message added\n"
                    elif self.identifying_message(3)=="add announcement":
                        messageData.EditMessage(5,'Replay',message)
                        response = "Announcement update successfully"
                        return response+"\n"
                    else:
                        pass
                else:
                    response = "invalid message do you want see command list(yes/no)"
                    if message.__contains__('yes'):
                        response = messageData.getCommandlist("admin")
                        return response + "\n"
                    elif message.__contains__('no'):
                        return "AS you Wish\n"
                    else:
                        pass
                    return response + "\n"

    def message_process(self, message: str):
        chatbox = self.driver.find_element(By.XPATH,
                                           '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
        if message == "":
            response = self.prepared_response(message)
            chatbox.send_keys(str(response))
            self.send_image()
        else:
            response = self.prepared_response(message)
            chatbox.send_keys(response)
        self.close_chat()
        feat.PrintDetails("BOT", 'USER')
        feat.PrintDetails(response, "MESSAGE")

    def send_image(self):
        filepath = r"D:\BCA\BCA VI\Project\Whatsapp Bot\assets\test.jpg"

        sleep(2)
        attech = self.driver.find_element(By.XPATH,
                                          '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')
        attech.click()
        image_box = self.driver.find_element(By.XPATH,
                                             '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input')
        image_box.send_keys(filepath)
        sleep(10)
        send_box = self.driver.find_element(By.XPATH,
                                            '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')
        send_box.click()
        sleep(2)

    def close_chat(self):
        self.Waiter.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/div/div')),
            "not found close menu in chat ").click()
        self.Waiter.until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[1]/div[1]/span[4]/div/ul/div/div/li[3]/div[1]')),
            "not found close chat element in Menu").click()
        # feat.PrintDetails("CHAT CLOSED", "INFO")

    def Run(self):
        feat.printBio()
        self.driver.get("https://web.whatsapp.com/")
        # WAIT FOR LOADING SIDE TILL 10 SECS.
        self.Waiter.until(EC.title_is("WhatsApp"))
        try:
            if len(self.driver.find_elements(By.CLASS_NAME, "_2UwZ_")) == 1:
                sleep(1)
                qrcodeelement = self.driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div')
                code = qrcodeelement.get_attribute("data-ref")
                pyperclip.copy(code)
                feat.PrintDetails("QR CODE TEXT COPIED GENERATE AND SCAN THE QR CODE ", "INFO")
        except:
            feat.PrintDetails("QR CODE SCANNED", "INFO")

        while True:
            if not self.search_chat():
                sleep(1)
                continue
            try:
                message = self.identifying_message()
                if message is None:
                    continue
                self.message_process(message)
            except:
                feat.PrintDetails("MESSAGE NOT FOUND", "ERROR")


wb = WhatsappBot()
wb.Run()
