import time
from bs4 import BeautifulSoup
import requests
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

s=Service(ChromeDriverManager().install())

def getanswer(l):
    driver = webdriver.Chrome(service=s)
    global_dynamicUrl = "https://tools.usps.com/zip-code-lookup.htm?byaddress"
    driver.get(global_dynamicUrl)
    driver.find_element(By.ID, 'tCompany').send_keys(l[0])
    driver.find_element(By.ID, 'tAddress').send_keys(l[1])
    driver.find_element(By.ID, 'tCity').send_keys(l[2])
    Select(driver.find_element(By.ID, 'tState')).select_by_value(l[3])
    driver.find_element(By.ID, 'tZip-byaddress').send_keys(l[4])
    driver.find_element(By.ID, 'zip-by-address').click()
    time.sleep(3)
    if driver.find_elements(By.XPATH, '//div[@class="zip_code_address unused-hide"]'):
        driver.close()
        return True
    if driver.find_elements(By.XPATH, '//div[@class="server-error address-tAddress help-block"]'):
        driver.close()
        return False
        
html = requests.get("https://docs.google.com/spreadsheets/d/1H1a9eBamflt3w-4BPEk1kJYc4VgsDBWlDjkS0hV5tAY/edit").text
soup = BeautifulSoup(html, "lxml")
table = soup.find_all("table")[0]
with open("addresses.csv", "w", encoding="utf-8", newline='') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    a = table.find_all("tr")[1].find_all("td")
    b = []
    for td in a:
        if td.text:
            b.append(td.text)
        else:
            break
    b.append("IsValid")
    wr.writerow(b)
    #wr.writerow([td.text for td in a if td.text].append("IsValid"))
    for row in table.find_all("tr")[2:]:
        if row.text:
            l = [td.text for td in row.find_all("td") if td.text]
            l.append(getanswer(l))
            wr.writerow(l)
        else:
            break
    #wr.writerows([[td.text for td in row.find_all("td") if td.text] for row in table.find_all("tr")[1:]])
