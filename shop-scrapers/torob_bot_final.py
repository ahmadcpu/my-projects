'''
this script will collect all the torob website businesses information and store them as an excel file.
'''
# importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd

# creating the dataframe
shop_cols = ['shop name', 'address', 'phone number', 'website domain', 'email address', 'mobile number(s)']
torob_shops = pd.DataFrame(columns=shop_cols)

chrome_options = Options()
chrome_options.headless = True # if you don't want to see the browser window set this variable True otherwise False

PATH = "D:\Program Files (x86)\chromedriver.exe" ############# path of chromedriver.exe #############

# setting up the webdriver
driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get(f'https://torob.com/shop-list/')
load_time = 20


# getting the last shop on torob website
script = WebDriverWait(driver, load_time).until(
        EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
).get_attribute('innerHTML')
content = json.loads(script)
last_shop = content['props']['pageProps']['shops'][0]['id']
        
for i in range(last_shop,2,-1):

        # the whole collecting data process from that page
        try:
                shop = {}
                driver.get(f'https://torob.com/shop/{i}/')
                script = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
                ).get_attribute('innerHTML')

                content = json.loads(script)
                shop_content = content['props']['pageProps']['shop']

                shop['shop name'] = shop_content['name']
                shop['address'] = shop_content['address']
                shop['phone number'] = shop_content['phone']
                shop['website domain'] = shop_content['domain']
        except:
                continue
        try:
                ems = shop_content['customer_support_info']['emails']
                emails = ' | '.join(i['email'] for i in ems)
                shop['email address'] = emails
        except:
                shop['email address'] = '-'
        try:
                phones = shop_content['customer_support_info']['phones']
                phone_numbers = ' | '.join(i['number'] for i in phones)
                shop['mobile number(s)'] = phone_numbers
        except:
                shop['mobile number(s)'] = '-'
        
        torob_shops = torob_shops.append(shop, ignore_index=True)
        if i % 30 == 0:
                # storing dataframe to an excel file because if for some reason the program 
                # stopped we dont want to lose the data we collected until that time
                torob_shops.to_excel('torob_shops.xlsx',index=False)


# storing dataframe to an excel file    
torob_shops.to_excel('torob_shops.xlsx',index=False)

print('finished')
driver.quit()



