"""
Uses Selenium to load the javascript and

"""


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from imgpull import pixiv_page_scrape
import os
import errno
import threading
import zipfile
import shutil


num = 1
page_add = "&p="
CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome("E:\Downloads\chromedriver.exe", options=chrome_options)
wait = WebDriverWait(driver, 100)


"""
    :param user_url: url for the user's profile page 
    :param user_path: where to download the images
    :param file_name: name of the file to zip to
"""
def main(user_url, user_path, file_name):
    driver.get(url)
    driver.find_element_by_class_name("signup-form__submit--login").click()

    user = driver.find_element_by_css_selector("#LoginComponent > form > div.input-field-group > div:nth-child(1) > input[type=text]")
    pwd = driver.find_element_by_css_selector("#LoginComponent > form > div.input-field-group > div:nth-child(2) > input[type=password]")

    user.send_keys("awesomeof07@gmail.com") #Enter username here
    pwd.send_keys("funguy1")   #Enter password here

    driver.find_element_by_xpath('//*[@id="container-login"]//*[@class="signup-form__submit"]').click()

    if not os.path.exists(os.path.dirname(user_path)):
        try:
            os.makedirs(os.path.dirname(user_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    wait.until(
        EC.presence_of_element_located((By.XPATH, './/*[@class="_2WwRD0o _2WyzEUZ"]')))
    page_access(user_url.rstrip(), user_path, 1, file_name)


"""
    :param url: the url of the profile page
    :param path: the path to download the image
    :param num: the starting page for the url
    :param zip: name of the zip file to zip to
"""
def page_access(url, path, num, zip):
    downloads = []
    last_page = int(driver.find_elements_by_class_name('_2m8qrc7')[-2].get_attribute('innerHTML'))
    while num <= last_page:
        page_url = url + page_add + str(num)
        try:
            driver.get(page_url)
            print(page_url)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="_2WwRD0o _2WyzEUZ"]//*[contains(@class,"sc-fzXfPN iGQfoW")]')))
            tags = driver.find_elements_by_xpath('//*[@class="_2WwRD0o _2WyzEUZ"]//*[contains(@class,"sc-fzXfPN iGQfoW")]')
            for tag in tags:
                # pixiv_page_scrape(tag.get_attribute("href"), path)
                downloads.append(threading.Thread(target=pixiv_page_scrape,args=(tag.get_attribute("href"), path)))
                downloads[-1].start()
        except OSError as exc:
            break
        num += 1
    driver.quit()
    for download in downloads:
        download.join()

    zip_path = os.path.dirname(path)
    zip_path = os.path.dirname(zip_path)
    print(path)
    file_paths = retrieve_file_paths(path)
    zip_file = zipfile.ZipFile(zip_path+'\\' +zip+'.zip','w')
    with zip_file:
        for file in file_paths:
            print("Zipping: ", file, "into: ", zip+'.zip')
            zip_file.write(file, os.path.basename(file), compress_type=zipfile.ZIP_STORED)
    shutil.rmtree(path)


"""
    :param dirName: the directory path
    :return all files in the directory
"""
# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
    # setup file paths variable
    file_paths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)

    # return all paths
    return file_paths


if __name__ == "__main__":
    url = input("Please input the url: ")
    file_name = input("Please input the file name: ")
    path = 'E:\\Documents\\3D\\Gallery\\' + "tmp\\"
    main(url, path, file_name)