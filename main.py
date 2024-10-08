from selenium import webdriver
from selenium .webdriver.chrome.service import Service
import time

service =Service(execute_path="chromedriver.exe")
driver = webdriver.chrome(service=service)
driver.get("https://google.com")
time.sleep(10)

driver.quit()