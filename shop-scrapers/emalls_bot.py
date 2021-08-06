'''
this script will collect all the emalls website shops's information and store them as an excel file
'''

# importing libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# creating the dataframe
emalls_shops = pd.DataFrame(columns=['shop name', 'adress', 'phone number', 'website domain', 'email adress'])

# last page's number
emalls_html = requests.get('https://emalls.ir/Shops').text
soup = BeautifulSoup(emalls_html, 'lxml')
last_page = int(soup.find(id='ContentPlaceHolder1_rptPagingBottom_hlinkPage_6').text)

# the first page you want to start scraping from
page = 1


while page < last_page + 1:
    try:
        # getting a page that contains some emalls shops
        emalls_html = requests.get(f'https://emalls.ir/Shops/page.{page}/').text
        soup = BeautifulSoup(emalls_html, 'lxml')

        # number of shops in that page
        shops = soup.find_all(class_='item')
        n_shops = len(shops)

        # getting some information about that page shops and storing them in the dataframe we created before
        for shop in shops:
            shop_content = {}
            shop_url = 'https://emalls.ir/' + shop.find('a')['href']

            shop_res = requests.get(shop_url).text
            shop_soup = BeautifulSoup(shop_res, 'lxml')
            
            contents = shop_soup.find(id='DivShops').find_all('tr')

            shop_content['shop name'] = shop_soup.title.text[11:-11]
            shop_content['adress'] = contents[1].find_all('td')[1].text
            shop_content['phone number'] = contents[2].find_all('td')[1].text
            shop_content['website domain'] = contents[5].find_all('td')[1].text
            shop_content['email adress'] = contents[6].find_all('td')[1].text.replace(' [at] ','@').replace(' [dot] ', '.')

            emalls_shops = emalls_shops.append(shop_content, ignore_index=True)

        # storing dataframe to an excel file because if for some reason the program stopped we dont want to lose
        # the data we collected until that time
        emalls_shops.to_excel('emalls_shops.xlsx', index=False)
        
    except:
        print(f'something went wrong on page {page}.')
    finally: page += 1

# storing dataframe to an excel file
emalls_shops.to_excel('emalls_shops.xlsx', index=False) 

print('finished.')
