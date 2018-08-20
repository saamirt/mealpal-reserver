from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import datetime
from win10toast import ToastNotifier
from mealpal_login import *

toaster = ToastNotifier()

def scroll_to_bottom():
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

chrome_options = Options()
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://mealpal.com/login")
driver.get("https://secure.mealpal.com/login")

try:
    user_email = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "user_email"))
    )
    user_email.send_keys(mealpal_user)
except Exception as error:
    print(error)
    print("could not find the email field")

try:
    user_password = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "user_password"))
    )
    user_password.send_keys(mealpal_pwd)
    user_password.submit()
except:
    print("could not find the password field")

print(datetime.datetime.now().time())
while(datetime.datetime.now().time() < datetime.time(17,0)):
    print("Not Time Yet")
    time.sleep(1)
print("Its time now")
driver.get("https://secure.mealpal.com/lunch")

scroll_to_bottom()

try:
    searchPath = "//div[@class='restaurant']/div[contains(@class, 'name') and normalize-space(text()) = 'The Poke Box']/ancestor::*[contains(@class,'meal-box')]"
    restaurants = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, searchPath))
    )
    restaurant = driver.find_element_by_xpath(searchPath)
    print('found restaurant')
    try:
        sold_out = restaurant.find_element_by_xpath(".//*[contains(@class,'fade-box-sold-out')]")
        print('sold out')
        toaster.show_toast('MealPal Sold Out','The Poke Box is sold out', icon_path = 'mealpal.ico', duration=10)
    except:
        print("not sold out")
    reserve_dialog = restaurant.find_element_by_xpath(".//*[contains(@class,'fade-box--meal-overlay')]")
    print('found reserve lunch dialog')
    meal_name = restaurant.find_element_by_xpath(".//div[contains(@class,'meal-name')]").get_attribute("textContent")
    print('Meal name : ' + meal_name)
    meal_desc = reserve_dialog.find_element_by_xpath(".//div[contains(@class,'description')]").get_attribute("textContent")
    print('Meal description : ' + meal_desc)
    dropdown = reserve_dialog.find_element_by_xpath(".//ul[contains(@class,'pickupTimes-list')]/*[normalize-space(text()) = '12:00 PM-12:15 PM']")
    print('found dropdown')
    driver.execute_script("$(arguments[0]).click();", dropdown)
    print('clicked dropdown option')
    reserve_btn = reserve_dialog.find_element_by_xpath(".//button[contains(@class,'mp-reserve-button')]")
    print('found reserve button')
    driver.execute_script("$(arguments[0]).click();", reserve_btn)
    print('clicked reserve button')
    with open('mealpal details for ' + (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + '.txt','w') as f:
        text = 'Meal Name: ' + meal_name
        text += '\nMeal Ingredients: ' + meal_desc
        text += '\nRestaurant: The Poke Box'
        text += '\nTime: 12:00 PM-12:15 PM'
        f.write(text)
    time.sleep(5)
    try:
        ticket = driver.find_element_by_xpath("//*[contains(@class,'meal-reservation__pickup-ticket')]/span")
        ticket_img_text = ticket.find_element_by_xpath("./img").get_attribute('ng-alt')
        print(ticket_img_text)
        ticket_num = ticket.text
        print(ticket_num)
        toaster.show_toast('MealPal Reserved',meal_name + '\nMealPal Ticket : ' + ticket_img_text + ' ' + ticket_num, icon_path = 'mealpal.ico', duration=10)
    except Exception as err:
        print("Could not find ticket number")
        print(err)
except Exception as e:
    print(e)

driver.quit()
