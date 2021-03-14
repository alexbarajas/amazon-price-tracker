import requests
from bs4 import BeautifulSoup
import smtplib

links = {  # you can add as many links as you want in this dictionary
    1: {"link": "FIRST LINK", "ideal_price": INT},
    2: {"link": "SECOND LINK", "ideal_price": INT}
}


def make_email():
    email = ""
    for key, value in links.items():
        AMAZON_HEADERS = {
            "Accept-Language": "en-us",
            "User-Agent": "UNIQUE TO YOU"
        }

        URL = value["link"]
        ideal_price = value["ideal_price"]

        response = requests.get(URL, headers=AMAZON_HEADERS)
        webpage_html = response.content  # .content returns binary data, while .text returns unocode data
        soup = BeautifulSoup(webpage_html, "lxml")  # using lxml is faster than html.parser
        
        item_name = soup.find(name="span", class_="a-size-large product-title-word-break").getText()
        item_price = soup.find(name="span", class_="a-size-medium a-color-price priceBlockBuyingPriceString").getText()
        price_float = float(item_price.split("$")[1])

        message = f"The price for {item_name.strip()} is cheaper than your ideal price by " \
                  f"${round((ideal_price - price_float), 2)}.\n\n" \
                  f"You can buy it at {URL}."
        if price_float < ideal_price:
            email += (message + "\n\n")
    return email


def send_email(email):
    MY_EMAIL = "FROM EMAIL"
    MAIN_EMAIL = "TO EMAIL"
    PASSWORD = "FROM EMAIL PASSWORD"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:  # your email client might not be gmail so code accordingly
        connection.starttls()  # way of securing the connection to the email server
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MAIN_EMAIL,
            msg=f"Subject:You can get some deals today!\n\n" + email.rstrip(),
        )


send_email(make_email())
