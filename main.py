from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import re
from unicodedata import normalize
import messageData
import features as feat
import pyperclip
from os.path import abspath


class WhatsappBot:
    driver = None
    username = None
    def __init__(self):
        opt = webdriver.ChromeOptions()
        # for chrome
        path = abspath("Default")
        opt.add_argument("--user-data-dir="+path)
        opt.headless = False
        #chromedriver = ChromeDriverManager().install()
        #service = Service(chromedriver)
        self.driver = webdriver.Chrome(executable_path="./driver/chromedriver", options=opt)

    def search_chat(self):
        print("Searching chats")

        if len(self.driver.find_elements(By.CLASS_NAME, "zaKsw")) == 0:
            print("chat opened")

            message = self.identifying_message()
            if message is not None:
                return True

        chats = self.driver.find_elements(By.CLASS_NAME, "_3m_Xw")
        for chat in chats:
            print("detecting unread messages...")

            unread_chats = chat.find_elements(By.CLASS_NAME, "cfzgl7ar")

            if len(unread_chats) == 0:
                print("chat answered")
                continue

            element_name = chat.find_elements(By.CLASS_NAME, 'zoWT4')
            name = element_name[0].text.replace(" ", "")
            WhatsappBot.username = name
            print(name, "authorized to be served by bot")
            if feat.isUser(name):
                print()
            else:
                feat.addUser(name)
            chat.click()
            return True
        return False

    def identifying_message(self, element=1):


        element_box_message = self.driver.find_elements(By.CLASS_NAME, "Nm1g1")
        position = len(element_box_message) - element

        color = element_box_message[position].value_of_css_property("background-color")

        if color == "rgba(220, 248, 198, 1)" or color == "rgba(5, 97, 98, 1)":
            print("chat identified")
            return

        element_message = element_box_message[position].find_elements(By.CLASS_NAME, "_1Gy50 ")
        message = element_message[0].text.lower()

        print("message recieved..", message)
        return self.normalizer(message)

    def normalizer(self, message: str):
        message = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
            normalize("NFD", message), 0, re.I
        )

        return normalize("NFD", message)

    def prepared_response(self, message: str):


        print("prepared responses")
        data = messageData.MessageLoad()
        if not feat.isAdmin(WhatsappBot.username):
            for index in data:
                if message.__contains__(index['message']):
                    response = index['Replay']
                    return response
            else:
                response = "invalid message do you want see command list(yes/no)"

                if self.identifying_message(2) != response:
                    return response + "\n"
                else:
                    if self.identifying_message(2) != "as your wish." and self.identifying_message() == "yes":
                        return messageData.commandlist
                    else:
                        return "as your wish.\n"
        else:
            for index in data:
                if message.__contains__(index['message']):
                    response = index['Replay']
                    return response
            else:
                admindata = messageData.MessageLoad("admin")
                for index in admindata:
                    if message.__contains__(index['message']):
                        response = index['response']
                        return response
                else:
                    response = "invalid message do you want see command list(yes/no)"
                    if self.identifying_message(2) != response:
                        return response+"\n"
                    else:
                        if self.identifying_message(2) !="as your wish." and self.identifying_message()=="yes":
                            return messageData.listofcommand
                        else:

                            return "as your wish.\n"

            # adminmessages = messageData.MessageLoad("admin")
            # for index in adminmessages:
            #     if message.__contains__(index['message']):
            #         response = index['response']
            #         return response
            # else:
            #     return "as your wish.\n"

        # else:
        #     if message.__contains__('add announcement'):
        #
        #         if feat.isAdmin(WhatsappBot.username):
        #             response = "what's your message?\n"
        #             return response
        #         else:
        #             response = "you have not right to change into bot :(\n"
        #             return response
        #     elif message.__contains__('add message'):
        #         if feat.isAdmin(WhatsappBot.username):
        #             response = "what would you add into user message ?\n"
        #             return response
        #         else:
        #             response = "you have not right to change into bot :(\n"
        #             return response
        #
        #     elif self.identifying_message(2) == "what would you add into user message ?":
        #         messageData.EditMessage(5, "Replay", message)
        #         response = "message updated\n"
        #         return response
        #
        #     elif self.identifying_message(2) == "what's your message?":
        #         messageData.EditMessage(5, "Replay", message)
        #         response = "message updated\n"
        #         return response
        #     elif self.identifying_message() == "shutdown":
        #         self.driver.quit()
        #         return ""
        #     else:
        #         response = "invalid command \n"
        # return response

    def message_process(self, message: str):
        chatbox = self.driver.find_element(By.XPATH,
                                           '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
        if message == "image":
            response = self.prepared_response(message)
            chatbox.send_keys(response)
            self.send_image()
        else:
            response = self.prepared_response(message)
            chatbox.send_keys(response)
        self.close_chat()

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
        openmenu = self.driver.find_element(By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/div/div')

        openmenu.click()
        sleep(1)
        close_chat = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/span[4]/div/ul/div/div/li[3]/div[1]')
        sleep(1)
        close_chat.click()
        print("chat closed")

    def Run(self):
        self.driver.get("https://web.whatsapp.com/")
        sleep(2)
        try:
            if len(self.driver.find_elements(By.CLASS_NAME, "_2UwZ_")) == 1:
                sleep(1)
                qrcodeelement = self.driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div')
                code = qrcodeelement.get_attribute("data-ref")
                pyperclip.copy(code)
                print(code)
                sleep(15)
        except:
            print("qr code scanned earlier")

        while True:

            if not self.search_chat():
                sleep(3)
                continue
            try:
                message = self.identifying_message()
                if message is None:
                    continue
                self.message_process(message)
            except:
                print("element not found")



wb = WhatsappBot()
wb.Run()
