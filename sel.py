from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
driver = webdriver.Chrome()
driver.set_page_load_timeout(10)
#driver.get("https://auth.zakon.kz/account/login")
driver.get("https://online.zakon.kz/ValidateAuth.aspx?token=zVrZY7DIt02n1j5ZETTw0g%3D%3D&tokenItem=jow1x74J2U%2BDgKNEWrUSXQ%3D%3D&returnUrl=")

#driver.get("https://online.zakon.kz/Document/Document.aspx?doc_id=39204650&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1")


all_cookies = driver.get_cookies()

for c in all_cookies:
    if c['name']=='SessionId':
        print c['value']

sys.exit('Done')

#assert "Python" in driver.title

elem = driver.find_element_by_name("Login")
elem.clear()
elem.send_keys("0595586181")

elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys("5634290166")



elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source


all_cookies = driver.get_cookies()

for c in all_cookies:
    if c['name']=='SessionId':
        print c['value']

assert "Python" in driver.title
driver.close()


