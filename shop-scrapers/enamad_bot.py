'''
this script will collect all the enamad website businesses information and store them as an excel file.
'''

# importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pandas as pd

# creating the dataframe
cols = ['title', 'website domain', 'address', 'phone', 'email address']
business_table = pd.DataFrame(columns=cols)

chrome_options = Options()
chrome_options.headless = True # if you don't want to see the browser window set this variable True otherwise False

PATH = "D:\Program Files (x86)\chromedriver.exe" ############ path of chromedriver.exe #############

# setting up the webdriver
driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get(f'https://enamad.ir/DomainListForMIMT/')
load_time = 20


# gettin the last page number
last_page_number = WebDriverWait(driver, load_time).until(
    EC.presence_of_element_located((By.CLASS_NAME, "PagedList-skipToLast"))
).find_element_by_tag_name('a').get_attribute("href").split("/")[-1]

last_page_number = int(last_page_number)
print(f"last page is: {last_page_number}")

number_of_rows = 30

page = 1 # the page you want to start scraping process

for page in range(1,last_page_number + 1):
    # getting page url to scrape
    driver.get(f"https://enamad.ir/DomainListForMIMT/Index/{page}")
    print(f'entering page: {page} ...')

    # if it's the last page we want to calculate the number of rows
    if page == last_page_number:
        print("it's the last page...")
        page_rows = WebDriverWait(driver, load_time).until(
            EC.presence_of_all_elements_located(By.CLASS_NAME, "row")
        )
        number_of_rows = int(len(page_rows)) - 8
    
    for i in range(number_of_rows):
        try:
            # the whole collecting data process from that page
            row = {}
            div_father = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.ID, "Div_Content"))
            )

            rows = div_father.find_elements_by_class_name('row')
            link = rows[i].find_elements_by_tag_name('a')[0]

            link.click()

            title = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            row['title'] = title.text[20:-1]
            

            domain = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, "domainlink"))
            ).text
            
            row['website domain'] = domain
            info_classes = driver.find_elements_by_class_name('mainul')[1].find_elements_by_class_name('row')[:-1]
            info = [i.find_elements_by_tag_name('div')[1].text for i in info_classes]
            row['address'] = info[0]
            row['phone'] = info[1]
            row['email address'] = info[2].replace('[at]', '@')
            
            business_table = business_table.append(row, ignore_index=True)
        except:
            # error handling
            print(f'error on page{page} and row {i+1}')
            driver.save_screenshot(f'error_in_page_{page}_row_{i+1}.png')
            print('screenshot saved successfully. you can view it now :.')
        
        finally:
            driver.back()

    # storing dataframe to an excel file because if for some reason the program stopped we dont want to lose
    # the data we collected until that time
    business_table.to_excel('enamad_table.xlsx', index=False)

    print(f'page {page} done successfully!')


# storing dataframe to an excel file
business_table.to_excel('enamad_table.xlsx', index=False)

print('finished.')
driver.quit()