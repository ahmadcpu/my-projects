'''
this script will collect all the torob website businesses information and store them as an excel file.
it's the same thing that {torob_bot_final.py} is. but it gets the last page from last_shops.json
and just add the last shops that we didn't add.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import json
import pandas as pd

shop_cols = ['shop name', 'address', 'phone number', 'website domain', 'email address', 'mobile number(s)']
torob_shops = pd.DataFrame(columns=shop_cols)

chrome_options = Options()
chrome_options.headless = True

PATH = "D:\Program Files (x86)\chromedriver.exe" ######### path of chromedriver.exe ########

driver = webdriver.Chrome(PATH, options=chrome_options)

load_time = 20

driver.get(f'https://torob.com/shop-list/')

script = WebDriverWait(driver, load_time).until(
        EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
).get_attribute('innerHTML')

content = json.loads(script)

last_shop = content['props']['pageProps']['shops'][0]['id']
#
json_file = open("last_shops.json")
last_shops = json.load(json_file)
last_in_xlsx = last_shops['last_torob']
last_shops['last_torob'] = last_shop

with open('last_shops.json', 'w') as j:
    json.dump(last_shops, j)

       
for i in range(last_shop,last_in_xlsx,-1):

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

# adding new shops to older ones
last_table = pd.read_excel('torob_shops.xlsx')
torob_shops = torob_shops.append(last_table)

torob_shops.to_excel('torob_shops.xlsx',index=False)

print('finished')
driver.quit()



