import requests
from twilio.rest import Client

STOCK_NAME = input("Enter your stock name like GOOGL , AAPL : ").upper()
COMPANY_NAME = input("Enter your company name: ").upper()

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everythingt"

stock_apikey = "STOCK_API_KEY"
news_api = "NEWS_API_KEY"
twillo_sid = "TWILLO_SID"
twillo_auth_token = "TWILLO_AUTH_TOKEN"
    

params = {
    "function":"TIME_SERIES_INTRADAY",
    "symbol":STOCK_NAME,
    "api_key":stock_apikey,

}
response = requests.get(url="https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=GOOGL&interval=5min&apikey=https://www.alphavantage.co/query",params=params)
data = response.json()



last_Day = data["Time Series (5min)"]
data_list = [value for (key,value) in last_Day.items() ]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)


day_before_yesterday_data = data_list[1]
day_before_yesterday_clsoing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_clsoing_price)


difference = abs(float(yesterday_closing_price)-float(day_before_yesterday_clsoing_price))
print(difference)


diff_percent = (difference/float(yesterday_closing_price))*100
print(diff_percent)



if diff_percent>0.14:
    new_params = {
        "api_key":news_api,
        "qintitle":COMPANY_NAME
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything?q=GOOGL&apiKey=b615f2d1fcbc439da6ae55f3ccabc267",params=new_params)
    articles = news_response.json()["articles"]
    
    
    three_articles = articles[:3]
    print(three_articles)

   
    
    formated_articles = [f"headline:{aritcle['title']}. \nbreif: {aritcle['description']}" for aritcle in three_articles]
  
    client = Client(twillo_sid,twillo_auth_token)
    for article in formated_articles:
        message = client.messages.create(body=article,from_="HERE_YOUR_TWILLO_NO",to="HERE_YOUR_SENDER_NO")

## msg format ##
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

