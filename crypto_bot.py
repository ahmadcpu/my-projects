'''
this script will alert you via windows notification and telegram bot when
the difference of some exchanges from https://tokenbaz.com/ website is more 
than the {percent} number that you tell to the file.
it also print some useful information about the proccess on your terminal.
to stop the program you need to do ctrl+C a couple of times.
'''

# importing libraries
import time
import datetime 
import requests
from bs4 import BeautifulSoup
import pandas as pd
from win10toast import ToastNotifier
toaster = ToastNotifier()

# setting up the telegram bot
user_id = "<user-telegram-id> type:<int>"
TOKEN = "<bot-token>"
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":user_id, "text":"start!"})


# getting percent
try: percent = float(input("enter the percent(default: 5): "))
except: percent = 5

# getting coins list
req = requests.get("https://tokenbaz.com/").text
soup = BeautifulSoup(req, 'lxml')
coins = soup.find(id="coin-list").find_all("li")[:-3]
coins_links = ["https://tokenbaz.com" + i.find("a")["href"] for i in coins]
coins_links.append("https://tokenbaz.com/compare-exchanges-prices/17/best-price-to-buy-and-sell-dash ")
coins_links.append("https://tokenbaz.com/exchanges?symbol=etc&label=%D8%A7%D8%AA%D8%B1%DB%8C%D9%88%D9%85-%DA%A9%D9%84%D8%A7%D8%B3%DB%8C%DA%A9")

# storing coin names
coin_names = []
for i in coins_links[:-1]:
    end = i.split("-")[-1][:-1]
    if end == "ripple":
        coin_names.append("xrp")
    elif end == "cash":
        coin_names.append("bitcoin-cash")
    elif end == "coin":
        coin_names.append("binance-coin")
    else: coin_names.append(end)
coin_names.append("ethereum-classic")

counter = 1

while True:
    print("---")
    print(f"---round: {counter}")
    print("---")
    t3 = time.time()
    

    for e,link in enumerate(coins_links):

        coin_name = coin_names[e]
        try:
            
            print(f"coin name: {coin_name}")
            # TASK 1
            df = pd.read_html(link)
            d = df[0].iloc[:-1,1:-1]
            

            best_buy = float("".join(d.iloc[:, 1][0].split()[0].split(',')))
            print(f"best price you can sell: {best_buy}")

            values = []
            for i in d.iloc[:, 3]:
                values.append(float("".join(i.split()[0].split(','))))

            best_sell = min(values)
            print(f"best price you can buy: {best_sell}")

            # getting tether
            teth_df = pd.read_html("https://tokenbaz.com/compare-exchanges-prices/5/best-price-to-buy-and-sell-tether")
            teth_d = teth_df[0].iloc[:-1,1:-1]
            
            teth_values = []
            for i in teth_d.iloc[:, 3]:
                teth_values.append(float("".join(i.split()[0].split(','))))

            tether = min(teth_values)
            print(f"tether is: {tether}")

            x1 = ((best_buy-best_sell)/best_buy) * 100

            print(f"the percent of TASK 1: {x1}")
            # getting current time
            current_time = datetime.datetime.now()
            # notification
            if x1 > percent:
                print(f">>>>>>>>>>>>>  TASK 1 -> {coin_name} -> {current_time.hour}:{current_time.minute} -> percent: {x1}  <<<<<<<<<<<<<")
                toaster.show_toast("TASK 1", coin_name, duration=0)
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":user_id, "text":f"TASK 1: {coin_name} -> percent: {x1}"})            
            
            # TASK 2       
            bit_req = requests.get(f"https://coinmarketcap.com/currencies/{coin_name}/").text
            bit_soup = BeautifulSoup(bit_req, 'lxml')
            price = float(bit_soup.find(class_="priceValue___11gHJ").text.replace("$","").replace(",",""))
            print(f"price of {coin_name} in dollars: {price}")

            x2 = 100 - ((price * tether * 100) / best_sell)
            print(f"the pecent of TASK 2: {x2}")
            
            # getting current time
            current_time = datetime.datetime.now()
            # notification
            if abs(x2) > percent:
                print(f">>>>>>>>>>>>>   TASK 2 -> {coin_name} -> {current_time.hour}:{current_time.minute} -> percent: {x2}   <<<<<<<<<<<<<<")
                toaster.show_toast("TASK 2", coin_name, duration=0)
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":user_id, "text":f"TASK 2: {coin_name} -> percent: {x2}"})
        except:
            print("error on:",coin_name)
            
    counter += 1
            
    # sleep until next update
    t4 = time.time()
    runtime = 61 - (t4-t3)
    print(f"round finished in {t4-t3} seconds.")

    if runtime > 0:
        print(f"sleeping for {runtime} seconds...")
        time.sleep(runtime)

    