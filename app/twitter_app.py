import json
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud



#Utility Functions
def check_word_in_tweet(word, data):
    """Checks if a word is in a Twitter dataset's text.
    Checks text and extended tweet (140+ character tweets) for tweets,
    retweets and quoted tweets.
    Returns a logical pandas Series.
    """
    contains_column = data['text'].str.contains(word, case = False)
    contains_column |= data['extended_tweet-full_text'].str.contains(word, case = False)
    contains_column |= data['quoted_status-text'].str.contains(word, case = False)
    contains_column |= data['quoted_status-extended_tweet-full_text'].str.contains(word, case = False)
    contains_column |= data['retweeted_status-text'].str.contains(word, case = False)
    contains_column |= data['retweeted_status-extended_tweet-full_text'].str.contains(word, case = False)
    return contains_column


def plot_wordcloud(docx):
    mywordcloud = WordCloud().generate(docx)
    fig = plt.figure(figsize = (20,10))
    plt.imshow(mywordcloud, interpolation = 'bilinear')
    plt.axis('off')
    st.pyplot(fig)



#############################################################

#Fuction to read json
# Fxn to Save Uploaded File to Directory
# def save_uploaded_file(uploadedfile):
#     #uploadedfile.name = 'uploaded_file'
#     with open(os.path.join('uploaded_files',uploadedfile.name),'wb') as f:
#         f.write(uploadedfile.getbuffer())
# 	return st.success('Saved file {} successfully'.format(uploadedfile.name))


def save_uploaded_file(uploadedfile):
    uploadedfile.name = 'uploaded_file'
    with open(os.path.join('uploaded_files', uploadedfile.name), 'wb') as f:
        f.write(uploadedfile.getbuffer())
    return st.success('File saved successfully')

#Function to read uploaded JSON FILE
def json_reader():
    tweets = []

    with open(os.path.join('uploaded_files/uploaded_file'), 'r') as f:
        for line in f:
            try:
                tweets.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                pass # skip this line
    return tweets

#Function to convert uploaded JSON FILE to dataframe
def to_df(data):
    final_t = []
    for tweet in data:
        if 'extended_tweet' in tweet:
            tweet['extended_tweet-full_text'] = tweet['extended_tweet']['full_text']
        final_t.append(tweet)
    df = pd.DataFrame(final_t)
    return df


##############################################################################


# Main App Function
def twitter_application():
    with st.form(key = 'project_name_form'):
        col1, col2 = st.columns([3, 1])

        with col1:
            project_name = st.text_input('Please name your project')
        with col2:
            st.text('Send Data')
            submit_name = st.form_submit_button(label = 'Save')

    with st.expander('Stream Live Twitter Content'):
        st.text('This feature of the application will be ready in a future update.In the meantime you can upload a Twitter JSON.\nIn the mean I have written some code to help you gather data from twitter using your keywords of interest,\nand also convert the JSON to a Dataframe.\nFor the app uses pre-collected just for demonstration purposes' )
        st.text_input('Please type in the keywords of interest')


        json_file = st.file_uploader('Upload Twitter JSON', type = ['json'])

        if json_file is not None:
            #save_uploaded_file(json_file)

            file_to_work_with = json_reader()
            st.write(file_to_work_with)

            with st.expander('Sample of uploaded data'):
                tweets = to_df(file_to_work_with)
                dataframe = pd.DataFrame(tweets)
                #data = pd.DataFrame(file_to_work_with)
                #st.dataframe(dataframe)


    with st.expander('Upload a dataframe containing twitter data'):
        csv_file = st.file_uploader('Upload Twitter CSV', type = ['csv'])
        if csv_file is not None:
            save_uploaded_file(csv_file)
        else:
            st.warning('Please select file to upload')

    if csv_file:
        df = pd.read_csv(csv_file)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df = df.set_index(['created_at'])

        #Plotting Mentions over time
        #create a python column
        df['python'] = check_word_in_tweet('#python', df)

        #create a rstats column
        df['rstats'] = check_word_in_tweet('#rstats', df)
        # Average of python column by day
        mean_python = df['python'].resample('1d').mean()

        # Average of rstats column by day
        mean_rstats = df['rstats'].resample('1d').mean()

        fig = plt.figure()
        plt.plot(mean_python.index.day, mean_python, color = 'green')
        plt.plot(mean_rstats.index.day, mean_rstats, color = 'blue')

        # Add labels and show
        plt.xlabel('Day'); plt.ylabel('Frequency')
        plt.title('Language mentions over time')
        plt.legend(('#python', '#rstats'))


        #Plotting Sentiments Over time
        sid = SentimentIntensityAnalyzer()
        # Generate sentiment scores
        sentiment_scores = df['text'].apply(sid.polarity_scores)
        df['sentiment'] = sentiment_scores
        df['sentiment'] = df.apply(lambda row: row['sentiment']['compound'], axis = 1)
        fig2 = plt.figure()


        # Plot average #python sentiment per day
        # Generate average sentiment scores for #python
        sentiment = df['sentiment']
        sentiment_py = sentiment[ check_word_in_tweet('#python', df) ].resample('1 d').mean()

        # Generate average sentiment scores for #rstats
        sentiment_r = sentiment[ check_word_in_tweet('#rstats', df) ].resample('1 d').mean()
        plt.plot(sentiment_py.index.day, sentiment_py, color = 'green')

        # Plot average #rstats sentiment per day
        plt.plot(sentiment_r.index.day, sentiment_r, color = 'blue')

        plt.xlabel('Day')
        plt.ylabel('Sentiment')
        plt.title('Sentiment of data science languages')
        plt.legend(('#python', '#rstats'))

        #removing urls from the text
        df['text'] = df['text'].str.replace('http\S+|www.\S+', '', case=False)
        tweet_list = []
        for tweet in df['text']:
            tweet_list.append(tweet)


        with st.expander('View Uploaded Data'):
            st.dataframe(df.head())


    if csv_file:
        col1, col2 = st.columns(2)
        with col1:
            with st.expander('Language Mentions Over Time'):
                st.info('This is a plot to show the number of times each language was mentioned over a period of 30days')
                st.pyplot(fig)


        with col2:
            with st.expander('Language Sentiments Over time'):
                st.info("Warning: This is Lit")
                st.pyplot(fig2)

    if csv_file:
        with st.expander('View WordCloud'):
            plot_wordcloud(str(tweet_list))
