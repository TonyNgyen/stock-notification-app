import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_KEY = "YGNH67R063FBOSIR"
NEWS_KEY = "4a8d74a17bf44fae8513496535073961"
TWILIO_SID = "AC3912104c7a9e64b712de208ddbad0c26"
TWILIO_AUTH_TOKEN = "82ee7030de08692667edaa104d1ca3f5"

STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY
}

NEWS_PARAMETERS = {
    "q": "Tesla",
    "apikey": NEWS_KEY
}

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

# Get yesterday's closing stock price
yday_closing = float(stock_data_list[0]["4. close"])

# Get the day before yesterday's closing stock price
before_yday_closing = float(stock_data_list[1]["4. close"])

# Find the positive difference between prices
stock_diff = yday_closing - before_yday_closing
up_down = None
if stock_diff > 0:
    up_down = "📈"
else:
    up_down = "📉"


# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
stock_diff_percent = round(stock_diff/before_yday_closing*100)


# percentage is greater than 5 then print("Get News").
if abs(stock_diff_percent) > 1:
    news_response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    news_data = news_response.json()
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

# Use Python slice operator to create a list that contains the first 3 articles.
    articles = news_data["articles"][:3]

# Send a separate message with each article's title and description to your phone number.

# Create a new list of the first 3 article's headline and description using list comprehension.
    text = [f"{STOCK_NAME}: {up_down}{stock_diff_percent}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in articles]

# Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in text:
        message = client.messages.create(
            body=article,
            from_="+18086454717",
            to="7148583631"
        )

