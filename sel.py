from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
driver = webdriver.Chrome()

driver.get("https://auth.zakon.kz/account/login")
#driver.get("https://online.zakon.kz/")

#sys.exit('Done')

#assert "Python" in driver.title

elem = driver.find_element_by_name("Login")
elem.clear()
elem.send_keys("0595586181")

elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys("5634290166")

driver.set_page_load_timeout(10)

elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source


all_cookies = driver.get_cookies()

for c in all_cookies:
    if c['name']=='SessionId':
        print c['value']

assert "Python" in driver.title
driver.close()


