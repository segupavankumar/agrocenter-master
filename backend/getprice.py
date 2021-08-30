import schedule
from bs4 import BeautifulSoup
import requests
import time
count = 0
def range_of_prices():
    global count
    print(count)    

    resul1 = requests.get(
        'https://market.todaypricerates.com/Andhra-Pradesh-vegetables-price')
    resul2 = requests.get(
        'https://market.todaypricerates.com/Andhra-Pradesh-fruits-price')

    soup1 = BeautifulSoup(resul1.content, 'html.parser')
    soup2 = BeautifulSoup(resul2.content, 'html.parser')

    table1 = soup1.find(class_="Table").get_text()
    table2 = soup2.find(class_="Table").get_text()

    with open("vege.txt", 'w', encoding='utf-8') as f:
        f.write(table1.strip())
        f.close()

    with open("frui.txt", 'w', encoding='utf-8') as f:
        f.write(table2.strip())
        f.close()
    count = count+1

schedule.every(1).days.do(range_of_prices)


while True:
    schedule.run_pending()
    time.sleep(1)