# import requests
# from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")


class AternosAPI():
    def __init__(self, common_cookies, srvcookie=None):
        self.driver = uc.Chrome(options=chrome_options)
        self.driver.get("http://aternos.org/s")
        self.driver.delete_all_cookies()
        for cookie in common_cookies:
            self.driver.add_cookie(common_cookies[cookie])
        if srvcookie:
            self.driver.add_cookie(srvcookie)
            self.driver.get("http://aternos.org/server")
        else:
            self.driver.get("http://aternos.org/servers")

    def ServerUpdate(self):
        server_infos = self.driver.find_elements(By.CLASS_NAME, "server-infos")
        sj = {}
        for server_info in server_infos:
            sj[server_info.find_element(By.CLASS_NAME, "server-title").find_element(By.CLASS_NAME, "server-name").text] = {
                "server_cookie": {
                    "name": "ATERNOS_SERVER",
                    "value": server_info.find_element(By.CLASS_NAME, "server-details").find_element(By.CLASS_NAME, "server-id").text[1:]
                }
            }
        return sj

    def GetStatus(self):
        status = self.driver.find_element(By.CLASS_NAME, "statuslabel-label").text
        self.driver.close()
        return status

    def StartServer(self):
        button = self.driver.find_element(By.ID, "start")
        if (status := self.driver.find_element(By.CLASS_NAME, "statuslabel-label")).text == "Offline":
            button.click()
            f = False
            while "Online" not in status.text: 
                if "Waiting in queue" in status.text and not f:
                    WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/div/div/div/header/span'))).click()
                    button = WebDriverWait(self.driver, 300).until(EC.element_to_be_clickable((By.ID, 'confirm')))
                    button.click()
                    f = True
                else:
                    if "Loading" in status.text:
                        return "server started"
                    elif "Starting" in status.text:
                        return "server started"
                    elif "Preparing" in status.text:
                        return "server started"
            self.driver.close()
            return "server started"
        else:
            self.driver.close()
            return "server is already online"

    def StopServer(self):
        button = self.driver.find_element(By.ID, "stop")
        if (status := self.driver.find_element(By.CLASS_NAME, "statuslabel-label")).text == "Online":
            button.click()
            while "Offline" not in status.text:
                if "Saving" in status.text:
                    return "server stopped"
                elif "Stopping" in status.text:
                    return "server stopped"
            self.driver.close()
            return "server stopped"
        else:
            self.driver.close()
            return "server is already offline"

    def GetServerInfo(self):

        self.driver.find_element(By.XPATH, "/html/body/div[2]/main/section/div[3]/div[1]/div/a").click()
        ipdata = self.driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div/div/main").text.split("\n")

        ip = ipdata[0].split(":")[1][1:]
        port = ipdata[1].split(":")[1][1:]

        Software = self.driver.find_element(By.ID, "software").text

        Version = self.driver.find_element(By.ID, "version").text

        Status = self.driver.find_element(By.CLASS_NAME, "statuslabel-label").text

        Players = "0/NA"

        if Status == "Online":
            Players = self.driver.find_element(By.XPATH, "/html/body/div[2]/main/section/div[3]/div[5]/div[2]/div[1]/div[1]/div[2]/div[2]").text
        self.driver.close()

        return {
            "ip": ip,
            "port": port,
            "software": Software,
            "version": Version,
            "status": Status,
            "players": Players
        }
