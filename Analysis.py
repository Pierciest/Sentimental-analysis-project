# -*- coding: utf-8 -*-
"""
import the libraries

"""

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import wordcloud as WordCloud
    import tweepy
    from textblob import TextBlob
    import numpy as np
    import re
    from bs4 import BeautifulSoup
    import requests
    from datetime import date, timedelta
    import os.path
except:
    print(
        "For the script to run please install pandas. Or you may also use 'pip install -r requirements.txt' in the command line opened inside the folder.")
    exit()
plt.style.use("fivethirtyeight")

"""Set the variables"""

page = 1
currency_titles = []
currency_titles_short = []

"""Find a page to get the currencies"""

topic_url = 'https://www.coingecko.com/en?page='

"""To obtain all the (100) pages put the topic_url in a loop, if the currencies are already been found just download it."""

E = 0
if os.path.isfile('Currencies.csv'):
    E = 1
else:
    E = 0

if E == 0:
    while page < 101:
        url = topic_url + str(page)
        response = requests.get(url)
        page_contents = response.text
        with open('Crypto_currencies.html', 'w', encoding="utf-8") as f:
            f.write(page_contents)
        with open('Crypto_currencies.html', 'r') as f:
            html_source = f.read()
        doc = BeautifulSoup(html_source, 'html.parser')
        selection_class = "tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between"
        currency_tags = doc.find_all('a', {'class': selection_class})
        for currency in currency_tags:
            currency_titles.append(currency.text.strip("\n"))
        selection_class2 = "tw-hidden d-lg-inline font-normal text-3xs ml-2"
        currency_tags_short = doc.find_all('span', {'class': selection_class2})
        currency_sub_titles_short = []
        for currency in currency_tags_short:
            currency_titles_short.append(currency.text.strip("\n"))

        page += 1
    currencies_dict = {
        "currency": currency_titles,
        "title": currency_titles_short
    }
    currencies_df = pd.DataFrame(currencies_dict)
    print(currencies_df)
    currencies_df.to_csv('Currencies.csv')
else:
    currencies_df = pd.read_csv("Currencies.csv")
    print(currencies_df)

"""Create a dictionary and show it to the user

Load the api data from Login.txt
"""

lines = []
with open('Login.txt') as f:
    lines = f.readlines()

consumerKey = lines[0].strip("\n")
consumerSecret = lines[1].strip("\n")
accessToken = lines[2].strip("\n")
accessTokenSecret = lines[3].strip("\n")

"""Create the authentication"""

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

"""Set the access token and the access token secret

"""

authenticate.set_access_token(accessToken, accessTokenSecret)

"""Create the API Object"""

api = tweepy.API(authenticate, wait_on_rate_limit=True)

"""Set the variables"""

Coin = int(input("Please choose a coin[0-9999] from the coins library of the tool: "))
Count = int(input("Please write the number of tweets you want to search for: "))
year = int(input('Enter a year: '))
month = int(input('Enter a month: '))
day = int(input('Enter a day: '))
Date = date(year, month, day)
CoinL = currencies_df["currency"][Coin]
CoinS = currencies_df["title"][Coin]

"""Arrange the date input by using the datetime library"""


def daterange(Date):
    today = date.today()
    for n in range(int((today - Date).days) + 1):
        yield Date + timedelta(n)


Dates = []
for dt in daterange(Date):
    Dates.append(dt.strftime("%Y-%m-%d"))

"""Gather the tweets about coins and filter out any retweets "RT"""

search_term = "#" + CoinL + "-filter:retweets"
search_term2 = "#" + CoinS + "-filter:retweets"

"""Create a cursor object

Search the tweets, The user id(Later we can use to get a detailed info about popularity),if verified or not, follwoer count and the creation date of the account
"""

all_tweets = []
all_users = []
all_verified = []
all_follower_count = []
all_creation_date = []
Lengths = []
Length = []
for i in Dates:
    tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang="en", since=i, tweet_mode="extended").items(Count / 2)
    tweets2 = tweepy.Cursor(api.search_tweets, q=search_term2, lang="en", since=i, tweet_mode="extended").items(Count / 2)
    # While writing on python make api.search, api.search_tweets
    for tweet in tweets:
        all_tweets.append(tweet.full_text)
        all_users.append(tweet.user.screen_name)
        all_verified.append(tweet.user.verified)
        all_follower_count.append(tweet.user.followers_count)
        all_creation_date.append(tweet.user.created_at)
        Length.append(tweet.full_text)

    for tweet in tweets2:
        all_tweets.append(tweet.full_text)
        all_users.append(tweet.user.screen_name)
        all_verified.append(tweet.user.verified)
        all_follower_count.append(tweet.user.followers_count)
        all_creation_date.append(tweet.user.created_at)
        Length.append(tweet.full_text)

    Lengths.append(len(Length))
    Length.clear()

print(all_tweets)
print(all_users)
print(all_verified)
print(all_follower_count)
print(all_creation_date)
print(Lengths)

"""Create a dataframe to store the tweets with columns called "Tweets", "Users", "Verified", "Followers", "Creation Date"."""

df = pd.DataFrame(
    {"Users": all_users, "Verified": all_verified, "Followers": all_follower_count, "Creation date": all_creation_date,
     "Tweets": all_tweets}, columns=['Users', 'Verified', 'Followers', 'Creation date', 'Tweets'])

"""Show the first 5 rows of data"""

df.head()
# Only to see if the program works so far

"""A function to find the popularity of the account the tweeted the tweet."""


def GetPopularity(follower, Verified):
    popularity = 0
    a = 0
    if follower <= 120:
        while a < follower:
            popularity += 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 100
        return popularity
    elif follower > 120 and follower <= 1000:
        a = 120
        popularity = 0.00000092
        while a < follower:
            popularity += 2 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 100
        return popularity
    elif follower > 1000 and follower <= 5000:
        a = 1000
        popularity = 0.00000092 + 880 * 2 * 7.7 * 10 ** -9
        while a < follower:
            popularity += 3 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 100
        return popularity
    elif follower > 5000 and follower <= 20000:
        a = 5000
        popularity = 1.4472 * 10 ** -5
        while a < follower:
            popularity += 5 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 100
        return popularity
    elif follower > 20000 and follower <= 50000:
        a = 20000
        popularity = 1.09644 * 10 ** -4
        while a < follower:
            popularity += 6 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 100
        return popularity
    elif follower > 50000 and follower <= 100000:
        a = 50000
        popularity = 1.495644 * 10 ** -3
        while a < follower:
            popularity += 2 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 100
        return popularity
    elif follower > 100000 and follower <= 500000:
        a = 100000
        popularity = 2.266 * 10 ** -3
        while a < follower:
            popularity += 3 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 90
        return popularity
    elif follower > 500000 and follower <= 1000000:
        a = 500000
        popularity = 0.014
        while a < follower:
            popularity += 1 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 15
        return popularity
    elif follower > 1000000 and follower <= 5000000:
        a = 1000000
        popularity = 0.016
        while a < follower:
            popularity += 4 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 15
        return popularity
    elif follower > 5000000 and follower <= 25000000:
        a = 5000000
        popularity = 0.14
        while a < follower:
            popularity += 3 * 7.7 * 10 ** -9
            a += 1
        if Verified == True:
            popularity = popularity * 3
        return popularity
    elif follower > 25000000 and follower <= 50000000:
        a = 25000000
        popularity = 0.6
        while a < follower:
            popularity += 1 * 7.7 * 10 ** -9
            a += 1
        return popularity
        if Verified == True:
            popularity = popularity * 3
    elif follower > 50000000:
        popularity = 1
        if Verified == True:
            popularity = popularity * 2
        return popularity


"""Create function to clean tweets


"""


def CleanTwt(twt):
    twt = re.sub(("#" + CoinL), CoinL, twt)  # Removes the hashtag from the coinL
    twt = re.sub(("#" + CoinS), CoinS, twt)  # Removes the hashtag from the coinS

    twt = re.sub("#" + (CoinL[0].capitalize() + CoinL[1:len(CoinL)]), (CoinL[0].capitalize() + CoinL[1:len(CoinL)]),
                 twt)  # Removes the hashtag from the coin
    twt = re.sub("#" + (CoinS[0].capitalize() + CoinS[1:len(CoinS)]), (CoinS[0].capitalize() + CoinS[1:len(CoinS)]),
                 twt)  # Removes the hashtag from the coin

    twt = re.sub("#[A-Za-z0-9]+", "", twt)  # Removes any strings with a hashtag
    twt = re.sub("\\n", "", twt)  # removing the "\n" character
    twt = re.sub("https?:\/\/\S+", "", twt)  # Removes any hyperlinks
    return twt


"""Clean the tweets"""

df["Cleaned_Tweets"] = df["Tweets"].apply(CleanTwt)

"""Show the dataset"""

df.head()
# Only to see if the program works so far

"""Create a function to get subjectivity"""


def getSubjectivity(twt):
    return TextBlob(twt).sentiment.subjectivity


"""Create a function to get the polarity"""


def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity


"""Create two new columns called subjectivity and polarity"""

df["Subjectivity"] = df["Cleaned_Tweets"].apply(getSubjectivity)
df["Polarity"] = df["Cleaned_Tweets"].apply(getPolarity)
data_object = zip(all_follower_count, all_verified)
Popularity = []
for i, b in data_object:
    Popularity.append(GetPopularity(i, b))
df["Popularity"] = Popularity

"""Show the data"""

df.head(10)
# Only to see if the program works so far

"""Create a function to get the sentiment text"""


def getSentiment(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


"""Create a column to store the text sentiment"""

df["Sentiment"] = df["Polarity"].apply(getSentiment)

"""Show the data"""

df.head(10)
# Only to see if the program works so far

"""Calculating the center of mass, Since each variable is between -1 and 1 the values are extremely small. To make them larger and obtain a readable data, Popularity*Subjectivity and Popularity*Polarity is extended by 10^3"""

Polarity = []
for i in df["Polarity"]:
    Polarity.append(i)
Subjectivity = []
for i in df["Subjectivity"]:
    Subjectivity.append(i)

Center_of_Mass = []

Popularity_Total = 0
d = 0
for i in Lengths:
    Popularity_divided = Popularity[d:d + i]
    Polarity_divided = Polarity[d:d + i]
    Subjectivity_divided = Subjectivity[d:d + i]

    for index in range(0, len(Popularity_divided)):
        Popularity_Total += Popularity_divided[index]
        PopSub = (Popularity_divided[index] * Subjectivity_divided[index] / Popularity_Total) * 10 ** 3
        PopPol = (Popularity_divided[index] * Polarity_divided[index] / Popularity_Total) * 10 ** 3
    Center_of_Mass.append(PopSub * PopPol)

    d += i

    Popularity_Total = 0
print(Center_of_Mass)

"""A scatter plot to see the data un organised"""

plt.figure(figsize=(8, 6))
for i in range(0, df.shape[0]):
    plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color="Purple")
plt.title("Sentiment analysis scatter plot")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity (Objective --> Subjective)")
plt.show()

"""Create a bar chart to show the count of negative positive and neutral tweets"""

df["Sentiment"].value_counts().plot(kind="bar")
plt.title("Sentiment analysis Bar plot")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")
plt.show()

"""A scatter plot to see the data in a more readable way."""

plt.figure(figsize=(10, 6))
for i in range(0, len(Dates)):
    plt.scatter(Dates[i], Center_of_Mass[i], color="Purple")
plt.title("Sentiment analysis scatter plot")
plt.xlabel("Dates")
plt.ylabel("Reliability point")
plt.show()
