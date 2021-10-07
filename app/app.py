import streamlit as st
import tweepy
from twitter_app import *
from news_app import *


#Configuring App Page
PAGE_CONFIG = {'page_title':'Decision Helper', 'page_icon': '🔥', 'layout': 'wide', 'initial_sidebar_state' :'expanded'}
st.set_page_config(**PAGE_CONFIG)

#APP CODE
def main():
    menu = ['About', 'Twitter', 'Stream News']
    choice = st.sidebar.selectbox('Select Activity', menu)

    if choice == 'About':
        st.subheader('About the App')
        st.write('This section provides a description of the Application and how it is supposed to be used. Have Fun! Get Insights From Twitter Data and News Articles. Open the sidebar and select an activity.\nIn the meantime the app is only for demonstration purposes.')
    elif choice == 'Twitter':
        st.subheader('Use Twitter Streams')
        twitter_application()

    else:
        st.subheader('Use News Data')
        stream_news()




if __name__ == '__main__':
    main()
