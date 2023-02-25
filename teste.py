from selenium import webdriver
import time

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://web.whatsapp.com")

time.sleep(1000)