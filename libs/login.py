from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_login_page(driver:webdriver.Chrome):
    LOGIN_URL = "https://login.yahoo.co.jp/config/login?.src=ym&.done=https%3A%2F%2Fmail.yahoo.co.jp%2F"

    try:
        driver.get(LOGIN_URL)
    except:
        raise Exception("Error: failed to get login page")

def send_username(driver:webdriver.Chrome,wait:WebDriverWait,username:str):

    username_id = "username"

    try:
        wait.until(EC.element_to_be_clickable((By.ID,username_id)))
    except:
        raise Exception("Error: Time out read user name page")
    
    try:
        driver.find_element(by=By.ID,value=username_id).send_keys(username)
    except:
        raise Exception("Error: faild to send user name")

    next_button_id = "btnNext"
    try:
        wait.until(EC.element_to_be_clickable((By.ID,next_button_id)))
    except:
        raise Exception("Error: Time out read next button")
    
    try:
        driver.find_element(by=By.ID,value=next_button_id).click()
    except:
        raise Exception("Error: faild to click next button")

def send_password(driver:webdriver.Chrome,wait:WebDriverWait,password:str):

    password_id = "passwd"

    try:
        wait.until(EC.element_to_be_clickable((By.ID,password_id)))
    except:
        raise Exception("Error: Time out read password page")
    
    try:
        driver.find_element(by=By.ID,value=password_id).send_keys(password)
    except:
        raise Exception("Error: faild to send password")
    
    login_button_id = "btnSubmit"

    try:
        wait.until(EC.element_to_be_clickable((By.ID,login_button_id)))
    except:
        raise Exception("Error: Time out read login button")
    
    try:
        driver.find_element(by=By.ID,value=login_button_id).click()
    except:
        raise Exception("Error: faild to click login button")

def login(driver:webdriver.Chrome,wait:WebDriverWait,username:str,password:str):
    get_login_page(driver)
    send_username(driver,wait,username)
    send_password(driver,wait,password)