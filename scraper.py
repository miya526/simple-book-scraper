# https://platform.virdocs.com/rscontent/epub/2321706/2486865/OEBPS/images/page-1.jpg
# coding=utf-8

#329
import time
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from PIL import Image
# python2.x, use this instead  
# from StringIO import StringIO
# for python3.x,
from io import BytesIO

email = "xxxxxx"
password = "xxxxxx"
 
driver = webdriver.Firefox()
driver.get("https://copycentral.redshelf.com/accounts/login/")

driver.find_element("id", "username").send_keys(email)

driver.find_element("id", "password").send_keys(password)

time.sleep(20)

driver.get("https://platform.virdocs.com/rscontent/epub/2321706/2486865/OEBPS/images/page-1.jpg")

# button = driver.find_element("class_name","btn btn-primary form-control")
# button.click()

s = requests.Session()
# Set correct user agent
selenium_user_agent = driver.execute_script("return navigator.userAgent;")
s.headers.update({"user-agent": selenium_user_agent})

for cookie in driver.get_cookies():
    s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
for page in range(1,330):
	website_name = "https://platform.virdocs.com/rscontent/epub/2321706/2486865/OEBPS/images/page-" + str(page) + ".jpg"
	response = s.get(website_name)
	image_name = "page-" + str(page) + ".jpg"
	i = Image.open(BytesIO(response.content))
	i.save(image_name)

