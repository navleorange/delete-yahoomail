from time import sleep
from typing import List
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from libs import scraping

def safety(driver:webdriver.Chrome):
    thread_class = "sc-2bd0h3-0 ghcBlZ ve2kc0-6 eYCQcj"
    thread_class = thread_class.replace(" ",".")
    super_elem = driver.find_element(by=By.CLASS_NAME,value=thread_class)
    
    checked_class = "sc-2bd0h3-0 keoCkY ve2kc0-4 dGena-d"
    checked_class = checked_class.replace(" ",".")
    
    if len(super_elem.find_elements(by=By.CLASS_NAME,value=checked_class)) > 0:
        super_elem.click()
        return False
    
    return True

def delete_mail_by_subject(driver:webdriver.Chrome,elems:List[WebElement],delete_subject:str,mail_table_class:str) -> bool:
    exist_flag = False
    unopened_mail_title_class = "sc-1dpypvu-11 bNqmhO"
    unopened_mail_title_class = unopened_mail_title_class.replace(" ",".")
    opened_mail_title_class = "sc-1dpypvu-11 krAOww"
    opened_mail_title_class = opened_mail_title_class.replace(" ",".")
        
    for elem in elems:
        mail_title = None

        is_exist_class = elem.find_elements(by=By.CLASS_NAME,value=unopened_mail_title_class)

        if len(is_exist_class) > 0:
            mail_title = is_exist_class[0].text
        else:
            is_exist_class = elem.find_elements(by=By.CLASS_NAME,value=opened_mail_title_class)
            if len(is_exist_class) > 0:
                mail_title = is_exist_class[0].text

        if mail_title == delete_subject:
            check_button_class = "ve2kc0-0 ve2kc0-1 dmeAlm"
            check_button_class = check_button_class.replace(" ",".")

            title = elem.find_element(by=By.CLASS_NAME,value=check_button_class).get_attribute("title")
            if title == "メール選択":
                elem.find_element(by=By.CLASS_NAME,value=check_button_class).click()
                exist_flag = True
                sleep(0.1)
        
        scraping.scroll_to_class(driver,mail_table_class,elem.rect["y"])
    
    return exist_flag

def push_delete_button(driver:webdriver.Chrome):
    one_delete_path = '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div[2]/ul[1]/li[3]/button'
    many_delete_path = '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div[2]/ul[1]/li[2]/button'
    delete_submit_class = "sc-1ns50jh-0 dmJYGP"
    delete_submit_class = delete_submit_class.replace(" ",".")

    is_exist_one_mail = driver.find_elements(by=By.XPATH,value=one_delete_path)
    is_exist_many_mail = driver.find_elements(by=By.XPATH,value=many_delete_path)

    if len(is_exist_one_mail) > 0 and is_exist_one_mail[0].text == "削除":
        driver.find_element(by=By.XPATH,value=one_delete_path).click()
        driver.find_element(by=By.CLASS_NAME,value=delete_submit_class).click()
    elif len(is_exist_many_mail) > 0 and is_exist_many_mail[0].text == "削除":
        driver.find_element(by=By.XPATH,value=many_delete_path).click()
        driver.find_element(by=By.CLASS_NAME,value=delete_submit_class).click()
    else:
        raise Exception("Error: failed to push delete button")

def empty_trash(driver:webdriver.Chrome):
    trash_delete_button_class = "sc-1ns50jh-0 kSjWiN sc-1gs1ku3-4 fdokAT"
    execute_empty_button_class = "sc-1ns50jh-0 dmJYGP"

    trash_delete_button_class = trash_delete_button_class.replace(" ",".")
    execute_empty_button_class = execute_empty_button_class.replace(" ",".")

    try:
        driver.find_element(by=By.CLASS_NAME,value=trash_delete_button_class).click()
        driver.find_element(by=By.CLASS_NAME,value=execute_empty_button_class).click()
    except:
        raise Exception("Error: failed to empty trash")

def execute_delete_mail(driver:webdriver.Chrome,wait:WebDriverWait,delete_subject:str):
    delete_flag = False
    trash_flag = False
    mail_table_class = "sc-9a4p4h-5 jDCkbO"

    scraping.use_filter(driver,wait,delete_subject)

    prev_elems = None

    while True:
        elems = scraping.fetch_mail_table(driver,wait,mail_table_class)

        if len(elems) <= 0:
            break

        exist_flag = delete_mail_by_subject(driver,elems,delete_subject,mail_table_class)
        delete_flag = delete_flag or exist_flag

        if delete_flag and safety(driver):
            push_delete_button(driver)
            trash_flag = True
            delete_flag = False

        if elems == prev_elems:
            break

        prev_elems = elems
    
    if trash_flag:
        empty_trash(driver)