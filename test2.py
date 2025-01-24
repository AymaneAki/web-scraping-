from bs4 import BeautifulSoup
import requests
import csv

url = "https://almostaphasmart.com/?product_cat=pc-gamer&per_row=4&shop_view=grid&per_page=24" 
response = requests.get(url)
# To verify if the request is succesful 
if(response.status_code != 200):
    print("Error")
    exit()

# Analyze HTML 
soup = BeautifulSoup( response.text ,"lxml")

csv_file = "almostapha_smart_laptops.csv"

laptop_titles = soup.find_all('h3', class_='wd-entities-title')
laptop_price = soup.find_all('span', class_='price')
n = len(laptop_titles)
list = []

for i in range(1, n):
    descp = laptop_titles[i].text.strip()
    price = laptop_price[i].find_all('span')
    if(len(price) > 2):
         d_price = price[2].text.strip()
    else:
         d_price = price[0].text.strip()

    list.append([descp, d_price])
    


with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['LAPTOP', 'PRICE'])
        writer.writerows(list)


