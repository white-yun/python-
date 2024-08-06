import requests
from bs4 import BeautifulSoup
import csv

# 目标网站的URL
url = 'https://bj.58.com/chuzu/'  # 58同城北京租房频道

# 发起HTTP请求，获取网页内容
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到包含房源信息的div元素
    listings = soup.find_all('li', class_='house-cell')

    # 打开CSV文件进行写入
    with open('rental_listings.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Location', 'Details'])

        # 提取每个房源的信息
        for listing in listings:
            title = listing.find('div', class_='des').find('h2').text.strip()
            price = listing.find('div', class_='money').find('b').text.strip()
            # location = listing.find('p', class_='add').find('a').text.strip()
            details = listing.find('div', class_='des').find('p').text.strip()

            # 写入CSV文件
            writer.writerow([title, price, details])

    print("Data has been successfully written to rental_listings.csv")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")