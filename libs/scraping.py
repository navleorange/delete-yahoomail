import time
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

def use_filter(driver:webdriver.Chrome,wait:WebDriverWait,keyword:str):
    search_filed_id = "searchfield"

    try:
        wait.until(EC.presence_of_element_located((By.ID,search_filed_id)))
    except:
        raise Exception("Error: Time out read search filed")

    try:
        driver.find_element(by=By.ID,value=search_filed_id).send_keys(keyword)
        driver.find_element(by=By.ID,value=search_filed_id).send_keys(Keys.ENTER)
    except:
        raise Exception("Error: failed to send keyword")
    
    time.sleep(2)

def scroll_page(driver:webdriver.Chrome,class_name:str,prev_html:str):
    SCROLL_WAIT_TIME = 0.5
    class_name = class_name.replace("."," ")

    driver.execute_script("document.getElementsByClassName('%s')[0].scrollTop = document.getElementsByClassName('%s')[0].scrollHeight;" % (class_name,class_name))

    current_html = driver.page_source


    if prev_html == current_html:
        return False
    else:
        time.sleep(SCROLL_WAIT_TIME)
        return True

def scroll_to_class(driver:webdriver.Chrome,table_class_name:str,height:int):
    driver.execute_script("document.getElementsByClassName('%s')[0].scrollTop += %s;" % (table_class_name,height))
    time.sleep(0.125)

def fetch_mail_table(driver:webdriver.Chrome,wait:WebDriverWait,mail_table_class:str) -> List[WebElement]:

    mail_table_class = mail_table_class.replace(" ",".")

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,mail_table_class)))
    except:
        raise Exception("Error: Time out read mail table")

    mail_table_selector = "#hotkeys > table > tbody > tr"

    try:
        elems = driver.find_elements(by=By.CSS_SELECTOR,value=mail_table_selector)
    except:
        raise Exception("Error: failed to get performance")

    return elems