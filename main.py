import requests
import smtplib
import os
from bs4 import BeautifulSoup

TARGET = 3500

MY_EMAIl = os.environ.get('M_EMAIL')
YOUR_EMAIL = os.environ.get('Y_EMAIL')
PASSWORD = os.environ.get('PASSWORD')

PRODUCT_URL = "https://www.amazon.pl/Apple-iPhone-14-128-GB/dp/B0BDK6YGFX/ref=sr_1_1_sspa"

headers = {
    "Accept-Language": "pl-PL,pl;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

response = requests.get(url=PRODUCT_URL, headers=headers)
amazon_webpage = response.text

soup = BeautifulSoup(amazon_webpage, "lxml")
price = soup.find(name="span", class_="a-price-whole").getText()
price = price.replace(",", "").split()
price = float(price[0] + price[1])

if price < TARGET:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIl, password=PASSWORD)

        connection.sendmail(from_addr=MY_EMAIl,
                            to_addrs=YOUR_EMAIL,
                            msg=f"Subject:Price for item you are looking for is below your target!\n\n"
                                f"Iphone 14 128GB is now only for: {price}PLN.\n"
                                f"Here is a link: {PRODUCT_URL}")
        connection.close()
