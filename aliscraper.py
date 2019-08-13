# This program tracks a products from AliExpress.com for lowering price
# And if products price is lowered this program will send you an email

import requests
from bs4 import BeautifulSoup
import smtplib
import time
import pandas as pd


# Place the products you want to track in wishlist.csv
# Use spaces as a delimiter
# Columns: product_url wanted_price
df = pd.read_csv('wishlist.csv', delimiter=' ')

headers = {
    "User-Agent": 'GOOGLE MY USER AGENT'}


def check_price(df_row):
    # Get URL from CSV table
    URL = df.product_url[df_row]

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(soup.prettify(), 'html.parser')

    title = soup.find("title").get_text().strip()
    print("\n\nProduct name: {title}".format(title=title))

    # Price is hidden in <script>. First we need to find price's location index
    scripts_list = soup.find_all('script')
    scripts_string = ''
    for i in scripts_list:
        scripts_string += str(i)
    price_index = scripts_string.find('formatedPrice')

    # Get and clean price. Code below is true for scraping from Russian IP
    price = int(scripts_string[price_index:price_index +
                               100].split("\":\"")[1].split(",")[0].replace('\xa0', ''))

    print("Price: {price} roubles".format(price=price))

    wanted_price = df.wanted_price[df_row]
    print("You want for {wanted_price} roubles".format(
        wanted_price=wanted_price))

    if(price <= wanted_price):
        send_mail()


def send_mail():
    # Connect to google
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Use google app password with 2-Step Verification or Less secure app access via usual password
    server.login('SENDING_EMAIL@gmail.com', 'PASSWORD')

    subject = 'Subject'
    body = 'Check the body with this link https://www.amazon.com/Xbox-One-1TB-Console-Minecraft-Bundle/dp/B07GRFQTM7/ref=sr_1_1?keywords=xbox&qid=1565286724&s=gateway&sr=8-1'

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'SENDING_EMAI@gmail.com',
        'RECIEVING@gmail.com',
        msg
    )
    print('Email has been sent!')


while(True):
    for i in range(len(df)):
        check_price(i)
    time.sleep(60*60*24)     # Checks once a day
