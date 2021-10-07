#Import streamlit
import streamlit as st
import streamlit.components.v1 as stc
#Extra imports
from twitter import run_twitter_api
from news import run_news_api


#PAGE CONFIGURATION
PAGE_CONFIG = {'page_title':'Deciapp', 'page_icon': '🔥', 'layout': 'wide', 'initial_sidebar_state' :'expanded'}
st.set_page_config(**PAGE_CONFIG)

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">DECIAPP</h1>
		<h4 style="color:white;text-align:center;">Get Help with decisions</h4>
		</div>
		"""

#APP CODE
stc.html(html_temp)
st.write("""
    ### Make Business Decisions by tracking keywords on Twitter and the News.
    Fill this section with more content.
    #### Twitter

    #### App Content
        - Twitter Insights
        - Insights from News
    #### How to use the App
        - First Point
        - Second Point
        - ...and so on
        - Click start when you ready.
    """)
def main():

    if st.button('START'):
        menu = ['Twitter', 'News Feed', 'About']
        choice = st.sidebar.selectbox('Pick a task', menu)

        if choice == 'Twitter':
            run_twitter_api()
        elif choice == 'News Feed':
            run_news_api()
        else:
            st.write('About')





if __name__ == '__main__':
    main()
