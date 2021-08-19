import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla"
API_KEY_STOCKS = "API_KEY"
API_KEY_NEWS = "API_KEY"
account_sid = "API_KEY"
auth_token = "API_KEY"

parameters_stocks = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCKS
}

response_stocks = requests.get("https://www.alphavantage.co/query", params=parameters_stocks)
response_stocks.raise_for_status()
data_stocks = response_stocks.json()
price_data = data_stocks["Time Series (Daily)"]

closing_price = {key: value["4. close"] for (key, value) in price_data.items()}
price_list = list(closing_price.values())

yesterday_price = float(price_list[0])
before_yesterday_price = float(price_list[1])
difference_percentage = round((yesterday_price - before_yesterday_price) / before_yesterday_price * 100)
up_down = None
if difference_percentage > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(difference_percentage) > 2:
    news_parameters = {
        "apiKey": API_KEY_NEWS,
        "qInTitle": COMPANY_NAME,
        "language": "en"
    }

    response_news = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    articles = response_news.json()["articles"]
    three_articles = articles[:3]

    article_list = [f"{STOCK}: {up_down}{difference_percentage}%.\nTitle: {article['title']}.\nPublished at: "
                    f"{article['publishedAt']}.\nURL: {article['url']}\n\n"
                    for article in three_articles]

    client = Client(account_sid, auth_token)

    for article in article_list:
        message = client.messages \
                        .create(
                             body=article,
                             from_='+17732506672',
                             to='TEL_NUMBER'
                         )
