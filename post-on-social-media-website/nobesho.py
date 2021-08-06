'''
this script will collect some information from nobesho website according to info.json and post them on
some social websites.[twitter, linkedin, pinterest, balatarin]
'''


# import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from time import sleep
import os
from bs4 import BeautifulSoup
import shutil
import json

# reading json file
json_file = open('info.json')
info = json.load(json_file)
json_file.close()

# getting current directory
current_dir = os.getcwd()

# setting up the webdriver
PATH = "D:\Program Files (x86)\chromedriver.exe"    ################ PATH #################
driver = webdriver.Chrome(PATH)
load_time = 20

# gettin information from json
page = info["info"]["page"]
category = info["info"]["category"]

try: shutil.rmtree(category)
except: pass

# collecting data from nobesho website
driver.get(f'https://www.nobesho.com/category/{category}')
driver.maximize_window()

start = info["info"]["start"]
finish = info["info"]["finish"]
loop_times = finish - start

links = []
titles = []
descriptions = []
picture_paths = []

directory = f'{category}/page_{page}/{start}_to_{finish}'

os.makedirs(directory)

page_button = WebDriverWait(driver, load_time).until(
    EC.presence_of_element_located((By.ID, page))
)
sleep(4)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

div_fathers = soup.find_all('div', class_='Products_Products__QW6ZW')[start:finish]

for e, div in enumerate(div_fathers):
    link = "https://nobesho.com" + div.findChildren('a')[0]['href']
    req = requests.get(link).text
    product_soup = BeautifulSoup(req, 'lxml')
    title = product_soup.find('h1').text

    description = ''
    ul = product_soup.find('div', class_="col-sm-6").findChildren('ul')[1]
    li_elements = ul.findChildren('li')
    for li in li_elements:
        description += li.text+ '\n'
    
    

    image_link = f'https://api.nobesho.com/v1/product_images/{link.split("/")[-1]}.jpg'
    with open(f'{directory}/{e}.jpg', 'wb') as im:
        im.write(requests.get(image_link).content)

    links.append(link)
    titles.append(title)
    descriptions.append(description)
    picture_paths.append(current_dir + f'\{directory}\{e}.jpg')
# end of collecting proccess


# class of posting the information we collected on social media websites
class post_on:
    
    # Post on twitter
    def twitter(self):
        USERNAME = info["twitter"]["twitter_username"]
        PASSWORD = info["twitter"]["twitter_password"]

        driver.get('https://www.twitter.com/login')

        user = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='session[username_or_email]']"))
        )
        user.send_keys(USERNAME)
        password = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='session[password]']"))
        )
        password.send_keys(PASSWORD)
        password.send_keys(Keys.RETURN)

        WebDriverWait(driver, 200).until(EC.title_contains("Home / Twitter"))

        sleep(2)

        for i in range(loop_times):
            circle = WebDriverWait(driver, load_time).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "circle"))
            )


            action = ActionChains(driver)
            action.double_click(on_element = circle[8])

            action.perform()

            spans = driver.find_elements_by_tag_name('span')


            spans[23].send_keys(f"{titles[i]}\n{links[i]}")
            spans[23].send_keys(Keys.RETURN)
        
            
            image_input = WebDriverWait(driver, load_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="fileInput"]'))
            )
            image_input.send_keys(picture_paths[i])

            tweet_button = WebDriverWait(driver, load_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='button']"))
            )[14]
            tweet_button.click()
    
    # Post on pinterest
    def pinterest(self):
        
        email = info["pinterest"]["pinterest_email"]
        password = info["pinterest"]["pinterest_password"]

        driver.get(f'https://www.pinterest.com/login')

        email_input = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))
        )
        email_input.send_keys(email)

        password_input = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        sleep(5)

        for i in range(loop_times):
            driver.get("https://pinterest.com/pin-builder/")
            picture_path = picture_paths[i]

            picture_input = WebDriverWait(driver, load_time).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
            )[1]
            picture_input.send_keys(picture_path)

            texts = WebDriverWait(driver, load_time).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "textarea"))
            )

            texts[0].send_keys(titles[i])
            texts[1].send_keys(links[i])

            save_button = WebDriverWait(driver, load_time).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Save')]"))
            )
            save_button.click()

            send_button = WebDriverWait(driver, load_time).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Send')]"))
            )

            send_button.click()

    # Post on balatarin
    def balatarin(self):
        driver.get('https://www.balatarin.com/login')

        USERNAME = info["balatarin"]["balatarin_username"]
        PASSWORD = info["balatarin"]["balatarin_password"]

        username_input = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.ID, "session_login"))
        )
        username_input.send_keys(USERNAME)

        password_input = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.ID, "session_password"))
        )
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)

        for i in range(loop_times):

            driver.get('https://www.balatarin.com/b/nobesho/submit')

            link_input = WebDriverWait(driver, load_time).until(
                    EC.presence_of_element_located((By.ID, "link_url"))
            )
            link_input.send_keys(links[i])

            title_input = WebDriverWait(driver, load_time).until(
                    EC.presence_of_element_located((By.ID, "link_title"))
            )
            title_input.send_keys(titles[i])

            description_input = WebDriverWait(driver, load_time).until(
                    EC.presence_of_element_located((By.ID, "link_description"))
            )
            description_input.send_keys(descriptions[i])

            tags = description_input = WebDriverWait(driver, load_time).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "tm-tag-remove"))
            )
            tags_number = len(tags)
            for i in range(0,tags_number * 2, 2):
                    driver.execute_script(f"document.getElementsByClassName('tm-tag-remove')[{i}].click()")

            driver.execute_script("document.querySelector(\"input[name=commit]\").click()")
            sleep(2)
        

    # Post on linkedin
    def linkedin(self):
        EMAIL = info["linkedin"]["linkedin_email"]
        PASSWORD = info["linkedin"]["linkedin_password"]

        driver.get('https://www.linkedin.com/')

        driver.maximize_window()

        email_input = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.ID, "session_key"))
        )
        email_input.send_keys(EMAIL)
        password_input = WebDriverWait(driver, load_time).until(
                EC.presence_of_element_located((By.ID, "session_password"))
        )
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)

        for i in range(loop_times):
                driver.execute_script("document.querySelectorAll(\"button\")[7].click()")



                text_dom = WebDriverWait(driver, load_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="ql-editor ql-blank"]'))
                )
                text_dom.click()

                text_input = WebDriverWait(driver, load_time).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
                )[0]
                text_input.send_keys(f'{links[i]}\n{descriptions[i]}\n{links[i]}')

                driver.execute_script("document.getElementsByClassName(\"artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view\")[1].click()") # picture select button

                picture_input = WebDriverWait(driver, load_time).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
                )[0]
                picture_input.send_keys(picture_paths[i])

                driver.execute_script("document.querySelectorAll(\"button[type='button']\")[1].click()") #done picture


                driver.execute_script("document.querySelector(\"button[aria-label='Save this post']\").click()") # post button

                driver.execute_script("document.querySelectorAll(\"button\")[0].click()")
# end of class




# calling the class and post the data we collected.

instance = post_on()

instance.twitter()
instance.linkedin()
instance.pinterest()
instance.balatarin()

