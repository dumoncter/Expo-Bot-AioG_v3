from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-crash-reporter")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-in-process-stack-traces")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--output=/dev/null")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")

browser = webdriver.Chrome()
pass_user = '1234'


def login():
    pass_button = 
    browser.find_element(By.XPATH, pass_button)
    password = browser.find_element(By.NAME, "0")
    password.send_keys(pass_user)
    b = '//input[@value="submit"]'
    browser.find_element(By.XPATH, b).send_keys(Keys.ENTER)
    time.sleep(2)


def reboot(ip):
    browser.get(ip)
    time.sleep(1)


def selenium_open(ip):
    login_url = "http://" + ip + "/setmed"
    browser.implicitly_wait(10)
    browser.get(login_url)
    login()


selenium_open("192.168.21.139")