#!/usr/bin/python





# 'https://snapshots.openflightmaps.org/live/2109/charts/efin/ef1/latest/ef1.pdf.zip'









# Requirements
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import sys
import getopt

default_download_dir = '/Data'
default_timeout = 120

def print_usage():
    print(f'Usage:')
    print(f'   {sys.argv[0]} [-o <output directory>] [-t <timeout in seconds>]')
    print(f'      -o <output directory> (default: {default_download_dir})')
    print(f'      -t <timeout in seconds> (default: {default_timeout})')

def main(argv):
    # Configuration
    timeout = default_timeout
    download_dir = default_download_dir

    try:
      opts, args = getopt.getopt(argv,"ho:t:",["outputdirectory=", "timeout="])
    except getopt.GetoptError:
      print_usage()
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print_usage()
         sys.exit()
      elif opt in ("-o", "--outputdirectory"):
         download_dir = arg
      elif opt in ("-t", "--timeout"):
         timeout = int(arg)
    print(f'Output directory is: {download_dir}')
    print(f'Request timeout is:  {timeout}')



    # Code
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized");
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('prefs',  {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
        }
    )

    def wait_for_downloads():
        while any([filename.endswith(".crdownload") for filename in os.listdir(download_dir)]):
            time.sleep(2)

    ##See: https://stackoverflow.com/a/60467435/1288109
    #class element_to_be_clickable(object):
    #    def __init__(self, element):
    #        self.element = element
    #
    #    def __call__(self, ignored):
    #        if self.element.is_displayed() and self.element.is_enabled():
    #            return self.element
    #        else:
    #            return False

    def download_data_in_page(driver, page_url):
      driver.get(page_url);
      # wait the ready state to be complete
      WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
      )
      WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'download_slogan')))
      button_download = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, 'download_slogan')))
      button_download.click()
      # wait the ready state to be complete
      WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
      )
      driver.find_element(By.ID, "languageEnglish").click()
      # wait the ready state to be complete
      WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
      )
      buttons = driver.find_elements_by_tag_name("button")
      for button in buttons:
        button_text = button.text.lower()
        if ('vfr' in button_text) or ('500' in button_text):
          #try:
          #  button.click()
          #except ElementClickInterceptedException as e:
          #  print(e)
          #  raise e

          #Attempt to prevent ElementClickInterceptedException
          #See: https://stackoverflow.com/a/48667924/1288109
          driver.execute_script("arguments[0].click();", button)

          # wait the ready state to be complete
          WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
          )
          section = driver.find_element(By.ID, "downloadContent0")
          section_buttons = section.find_elements_by_tag_name("button")
          for section_button in section_buttons:
            if section_button.text.startswith('Download'):
              #section_button.click()

              #Attempt to prevent ElementClickInterceptedException
              #See: https://stackoverflow.com/a/48667924/1288109
              driver.execute_script("arguments[0].click();", section_button)
          break

      return

    with webdriver.Chrome(options=options) as driver:
        driver.maximize_window();
        
        driver.get("https://www.openflightmaps.org/");
        driver.find_element(By.ID, "regionsTitle").click()
        #user_box = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/div[2]/ul[1]/li[6]/ul"]')))
        list_items = driver.find_elements_by_xpath('/html/body/nav/div/div[2]/ul[1]/li[6]/ul/li')

        print('fetching page URLs...')
        page_infos = {};
        for list_item in list_items:
          key =list_item.text;
          anchor = list_item.find_element_by_tag_name("a")
          page_url = anchor.get_attribute('href')
          page_infos[key] = {
            'url': page_url            
          }

        for key, value in page_infos.items():
            print(f'Processing {key}...')
            #directory_name = f'{download_dir}/{key}';
            #if not os.path.exists(directory_name):
            #  os.makedirs(directory_name) 
            download_data_in_page(driver, value['url'])

        
#        driver.find_element(By.ID, "14").click()
#        driver.find_element(By.ID, "download_slogan").click()
#
#        # user_box = WebDriverWait(driver, TIME_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/input[1]')))
#        user_box = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/div[2]/ul[1]/li[6]/ul"]')))
#        #user_box = WebDriverWait(driver, timeout).until(EC.elementToBeClickable((By.XPATH, '//*[@id="idcs-signin-basic-signin-form-username"]')))
#        user_box.click()
#        user_box.send_keys(user_name)
#
#        password_box = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/input[2]')))
#        password_box.click()
#        password_box.send_keys(password)
#        
#        
#        button = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/center/button')))
#        button.click()
#        
#        # wait the ready state to be complete
#        WebDriverWait(driver=driver, timeout=10).until(
#            lambda x: x.execute_script("return document.readyState === 'complete'")
#        )
#        
#        #print('Page source:')
#        #print(driver.page_source)
#
#        links = []
#        page_links = driver.find_elements_by_tag_name('a')
#        for link in page_links:
#            href = link.get_attribute('href')
#            if href is not None:
#                #print(href)
#                links.append(href)
#                
#        print('Downloading links:')
#        for link in links:
#            print(link)
#            driver.get(link)
#
        print('... waiting for all downloads to finish...')
        wait_for_downloads()
#        # print("output directory:")
#        # print(os.listdir(download_dir))
        print('... done.')
        driver.quit()

if __name__ == "__main__":
   main(sys.argv[1:])