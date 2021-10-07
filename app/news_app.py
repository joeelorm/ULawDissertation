import streamlit as st
from newsapi import NewsApiClient
import urllib.request
import requests
import bs4
import datetime as dt
import pandas as pd
from twitter_app import plot_wordcloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

#Initializations
my_api_key = '127932d3d2e44be5863405da08212ed8'
newsapi = NewsApiClient(api_key = my_api_key)
sid = SentimentIntensityAnalyzer()



#Function to retrieve news
def retrieve_news(keyword, from_date, to_date):
    data = newsapi.get_everything(q = keyword,  from_param = from_date, to = to_date, language = 'en')
    return data


#Function to retrieve full news content and save it in a column within the dataframe
def get_full_content(row):
    url = row['url']
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    for para in soup.find_all('p'):
        return para.get_text()

#Function to collect text from the full_text column of returned data frame
def collect_full_text(col):
    all_text = []
    for content in col:
        all_text.append(content)
    return(str(all_text))

#A Function to plot the sentiments
def sentiment_plotter(df, topic):
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df = df.set_index(['publishedAt'])
    sentiment_scores = df['full_content'].apply(sid.polarity_scores)
    df['sentiment'] = sentiment_scores
    df['sentiment'] = df.apply(lambda row: row['sentiment']['compound'], axis = 1)


    # Generate average sentiment scores for keyword
    resample_sents = df['sentiment'].resample('W').mean()
    #Plot the sentiments scores of the articles containg the keyword over the week

    # Plot average #python sentiment per day
    fig = plt.figure()
    plt.plot(resample_sents.index, resample_sents, color = 'red')


    plt.xlabel('Week')
    plt.ylabel('Sentiment')
    plt.title('Sentiment of {} across the chosen dates'.format(topic))
    plt.xticks(rotation = 45)
    #plt.legend(('#python', '#rstats'))
    st.pyplot(fig)








def stream_news():
    topic = st.text_input('What News Topic would you like to Explore')
    from_date = st.date_input('From:')
    to_date = st.date_input('To:')
    if st.button('Go'):
        if topic:
            news = retrieve_news(topic, from_date, to_date)
            articles = news['articles']
            df = pd.DataFrame(articles)
            df['full_content'] = df.apply(lambda row: get_full_content(row), axis = 1)
            with st.expander('List of News Articles'):

                st.write('Number of artcles retrieved: ', news['totalResults'])

                for article in articles:
                    st.write(article['title'])

            with st.expander('View DataFrame of collected news'):
                st.dataframe(df.head())

            with st.expander('View WordCloud'):
                all_text = collect_full_text(df['full_content'])
                plot_wordcloud(all_text)

            with st.expander('View Sentiments'):
                sentiment_plotter(df, topic)
