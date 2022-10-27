from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import config

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URLs
LOGIN_URL = "https://stage.outreach.sloovi.com/login"
TASK_PAGE_URL = "https://stage.outreach.sloovi.com/lead/lead_7e0ce02cc9854ceeb61ea58bbae3f2b6"
OPPORTUNITY_PAGE_URL = " https://stage.outreach.sloovi.com/lead/lead_7e0ce02cc9854ceeb61ea58bbae3f2b6"

valid_email = config.valid_email
valid_password = config.valid_password

# PATHs
login_button_path = '//*[@id="main"]/section/div[2]/form/div[2]/button'
delete_error_display_path = '//*[@id="main"]/div/div/div[2]/div[2]/div/div[2]'
email_field_path = '//*[@id="main"]/section/div[2]/form/label[1]/input'
password_field_path = '//*[@id="main"]/section/div[2]/form/label[2]/input'
home_icon_path = '//*[@id="main"]/div/div/div[1]/div/div/div/button/img'


def check_element_exists(element):
    try:
        driver.find_element(By.XPATH, element)
        return True
    except NoSuchElementException:
        return False


def user_login(email, password):
    driver.get(url=LOGIN_URL)

    email_field = driver.find_element(By.XPATH, email_field_path)
    email_field.send_keys(email)
    time.sleep(2)

    password_field = driver.find_element(By.XPATH, password_field_path)
    password_field.send_keys(password)
    time.sleep(2)

    login_button = driver.find_element(By.XPATH, login_button_path)
    login_button.send_keys(Keys.SPACE)
    time.sleep(5)


def verify_user_login(email, password):
    user_login(email, password)
    driver.implicitly_wait(10)
    return check_element_exists(home_icon_path)


def verify_task_view():
    user_login(valid_email, valid_password)
    driver.implicitly_wait(10)

    driver.get(url=TASK_PAGE_URL)
    driver.implicitly_wait(10)

    return check_element_exists(delete_error_display_path)


def verify_task_view_negative():
    driver.implicitly_wait(10)

    driver.get(url=TASK_PAGE_URL)
    driver.implicitly_wait(10)

    return check_element_exists(login_button_path)


def verify_opportunity_view():
    driver.implicitly_wait(10)

    user_login(valid_email, valid_password)
    driver.implicitly_wait(10)

    driver.get(url=OPPORTUNITY_PAGE_URL)
    driver.implicitly_wait(10)

    return check_element_exists(delete_error_display_path)


def verify_opportunity_view_negative():
    driver.implicitly_wait(10)

    driver.get(url=OPPORTUNITY_PAGE_URL)
    driver.implicitly_wait(10)
    return check_element_exists(login_button_path)


# TC_001 User can login with valid email and password
tc_001 = verify_user_login(valid_email, valid_password)
if tc_001:
    print("Test case 001 Passed ")
else:
    print("Test case 001 Failed ")
driver.close()

# # TC_002 User can NOT login with an  invalid email and valid password
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tc_002 = verify_user_login("negativetest@gmail.com", valid_password)

if not tc_002:
    print("Test case 002 Passed ")
else:
    print("Test case 002 Failed ")
driver.close()

# # TC_003 User can NOT login with a valid email and an invalid password
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tc_003 = verify_user_login(valid_email, "1357911")

if not tc_003:
    print("Test case 003 Passed ")
else:
    print("Test case 003 Failed ")
driver.close()


# # TC_004 User can NOT  login with invalid email and password
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tc_004 = verify_user_login("negativetest@gmail.com", "1357911")

if not tc_004:
    print("Test case 004 Passed ")
else:
    print("Test case 004 Failed ")
driver.close()


# # TC_005 Authenticated User can view Task page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tc_005 = verify_task_view()
if not tc_005:
    print("Test case 005 Passed ")
else:
    print("Test case 005 Failed ")
driver.close()


# # TC_006 Unauthenticated User can NOT  view Task page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tc_004 = verify_task_view_negative()
if tc_004:
    print("Test case 006 Passed ")
else:
    print("Test case 006 Failed ")
driver.close()


# # TC_007 Authenticated User can view opportunity page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tc_007 = verify_opportunity_view()
if not tc_007:
    print("Test case 007 Passed ")
else:
    print("Test case 007 Failed ")
driver.close()


# # TC_008 Unauthenticated User can NOT view Opportunity page
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tc_008 = verify_opportunity_view_negative()
if tc_008:
    print("Test case 008 Passed ")
else:
    print("Test case 008 Failed ")
driver.close()
