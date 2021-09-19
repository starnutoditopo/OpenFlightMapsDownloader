#!/usr/bin/python

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
import shutil
from itertools import islice, count

default_partials_dir = "/PartialFiles"
default_output_dir = "/Output"
default_timeout = 120


def print_usage():
    print(f"Usage:")
    print(
        f"   {sys.argv[0]} [-p <partial files directory>] [-o <output directory>] [-t <timeout in seconds>]"
    )
    print(f"      -p <partial files directory> (default: {default_partials_dir})")
    print(f"      -o <output directory> (default: {default_output_dir})")
    print(f"      -t <timeout in seconds> (default: {default_timeout})")


def main(argv):
    # Configuration
    timeout = default_timeout
    output_dir = default_output_dir
    partials_dir = default_partials_dir

    try:
        opts, args = getopt.getopt(
            argv, "hp:o:t:", ["partialfilesdirectory=", "outputdirectory=", "timeout="]
        )
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print_usage()
            sys.exit()
        elif opt in ("-p", "--partialfilesdirectory"):
            partials_dir = arg
        elif opt in ("-o", "--outputdirectory"):
            output_dir = arg
        elif opt in ("-t", "--timeout"):
            timeout = int(arg)
    print(f"Partial files directory is: {partials_dir}")
    print(f"Output directory is: {output_dir}")
    print(f"Request timeout is:  {timeout}")

    # Code
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # options.add_argument('window-size=1200x600')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": partials_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        },
    )

    def wait_for_downloads():
        while True:
            if any(
                [filename.lower().endswith(".crdownload") for filename in os.listdir(partials_dir)]
            ):
                #print('      still partial files exist: waiting...')
                time.sleep(3)
                continue
            if not any([filename.lower().endswith(".zip") for filename in os.listdir(partials_dir)]):
                #print('      no zip file exist: waiting...')
                time.sleep(3)
                continue
            break;

    ##See: https://stackoverflow.com/a/60467435/1288109
    # class element_to_be_clickable(object):
    #    def __init__(self, element):
    #        self.element = element
    #
    #    def __call__(self, ignored):
    #        if self.element.is_displayed() and self.element.is_enabled():
    #            return self.element
    #        else:
    #            return False

    def download_data_in_page(driver, region_name, page_url):
        driver.get(page_url)
        # wait the ready state to be complete
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "download_slogan"))
        )
        button_download = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "download_slogan"))
        )
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

        button_ids_of_interest = []
        buttons = driver.find_elements_by_tag_name("button")
        for idx, button in enumerate(buttons):
            button_text = button.text.lower()
            if ("vfr" in button_text) or ("500" in button_text):
                button_ids_of_interest.append(idx)

        for idx in button_ids_of_interest:
            # reload all buttons
            buttons = driver.find_elements_by_tag_name("button")
            button = next(islice(buttons, idx, None))
            # Attempt to prevent ElementClickInterceptedException
            # See: https://stackoverflow.com/a/48667924/1288109
            driver.execute_script("arguments[0].click();", button)

            # wait the ready state to be complete
            WebDriverWait(driver=driver, timeout=10).until(
                lambda x: x.execute_script(
                    "return document.readyState === 'complete'"
                )
            )
            
            section = driver.find_element(By.ID, "downloadContent0")
            section_button_ids_of_interest = []
            section_buttons = section.find_elements_by_tag_name("button")
            for section_button_idx, section_button in enumerate(section_buttons):
                if section_button.text.startswith("Download"):
                    section_button_ids_of_interest.append(section_button_idx)


            for section_button_idx in section_button_ids_of_interest:
                #reload section
                section = driver.find_element(By.ID, "downloadContent0")
                # reload all section buttons
                section_buttons = section.find_elements_by_tag_name("button")
                section_button = next(islice(section_buttons, section_button_idx, None))

                # section_button.click()

                # Attempt to prevent ElementClickInterceptedException
                # See: https://stackoverflow.com/a/48667924/1288109
                driver.execute_script("arguments[0].click();", section_button)
                WebDriverWait(driver=driver, timeout=10).until(
                    lambda x: x.execute_script(
                        "return document.readyState === 'complete'"
                    )
                )

                print("   ... waiting for download process to finish...")
                wait_for_downloads()
                print("   done.")
                region_directory_name = f"{output_dir}/{region_name}"
                if not os.path.exists(region_directory_name):
                    os.makedirs(region_directory_name)

                downloaded_files = os.listdir(partials_dir)
                for downloaded_file in downloaded_files:
                    if downloaded_file.lower().endswith(".zip"):
                        head, tail = os.path.split(downloaded_file)
                        print(f'   ... moving file "{tail}" to output folder...')

                        # Move and eventually overwrite the existing file
                        # See: https://stackoverflow.com/a/57911288/1288109
                        shutil.move(os.path.join(partials_dir, downloaded_file), os.path.join(region_directory_name, tail))
                        
                        print(f"   done.")

        return

    with webdriver.Chrome(options=options) as driver:
        driver.maximize_window()

        driver.get("https://www.openflightmaps.org/")
        driver.find_element(By.ID, "regionsTitle").click()
        # user_box = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/div[2]/ul[1]/li[6]/ul"]')))
        list_items = driver.find_elements_by_xpath(
            "/html/body/nav/div/div[2]/ul[1]/li[6]/ul/li"
        )

        print("Fetching region page URLs...")
        page_infos = {}
        for list_item in list_items:
            key = list_item.text
            anchor = list_item.find_element_by_tag_name("a")
            page_url = anchor.get_attribute("href")
            page_infos[key] = {"url": page_url}
        print(f"... done ({len(page_infos)} region pages fetched).")

        if not os.path.exists(partials_dir):
            print("Creating directory for partial files...")
            os.makedirs(partials_dir)
            print("... done.")


        for key, value in page_infos.items():
            print(f"Processing region: {key}...")
            download_data_in_page(driver, key, value["url"])
            print(f"done.")

        driver.quit()


if __name__ == "__main__":
    main(sys.argv[1:])
