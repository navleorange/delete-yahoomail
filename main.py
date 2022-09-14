import libs
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs

def driver_init() -> webdriver.Chrome:
  '''
    Webブラウザを操作するためのWebDriveの設定を行う

    Returns:
      webdriver.Chrome: 設定をしたdriverを返す
    
    Note:
      CHROMEDRIVER: ローカルでchromedriverを使用する場合に使用
      CHROME_DRIVER_PATH: herokuでchromedriverを使用する場合のパス
  '''
  #CHROMEDRIVER = '/opt/chrome/chromedriver'
  CHROME_DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'  #heroku driver path
  options = Options()
  options.add_argument('--headless')  
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')

  chrome_service = fs.Service(executable_path=CHROME_DRIVER_PATH)

  return webdriver.Chrome(service=chrome_service, options=options)

def main():
  '''
    学務情報システムから成績を読み込み、DBに存在しない場合はツイートして登録する

    Note:
      envファイルの設定が必要
  '''
  driver = driver_init()

  # time out 10s
  wait = WebDriverWait(driver,30)
  #driver.implicitly_wait(10)

  load_dotenv()
  username = os.getenv("USER_NAME")
  password = os.getenv("PASSWORD")
  libs.login(driver,wait,username,password)

  delete_subject = "学務情報システムからログインのお知らせ"
  libs.execute_delete_mail(driver,wait,delete_subject)
  time.sleep(10)

  driver.quit()

if __name__ == "__main__":
  main()