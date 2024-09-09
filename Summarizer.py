import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from newspaper import Article

# Ensure you have the required nltk resources
nltk.download('vader_lexicon')
nltk.download('punkt')

st.set_page_config(layout="wide")
# Set the main title with red color
st.markdown("<h1 style='color: #FF0000;'> ARTICLES | NEWS | URL : SUMMARIZER </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #00FFFF;'>Unlock the Power of Text Analysis: Summarize Articles, News, and Websites with a single click. Start now! </h3>", unsafe_allow_html=True)
def summarize(url):
    article = Article(url)

    # Download and parse the article
    article.download()
    article.parse()
    article.nlp()

    result = {}

    # Collect article data
    result['title'] = article.title
    result['authors'] = ", ".join(article.authors)
    result['publication_date'] = article.publish_date if article.publish_date else "Date of Publication Unavailable"
    result['summary'] = article.summary

    # Sentiment analysis
    sia = SentimentIntensityAnalyzer()
    SENTIMENT_scores = sia.polarity_scores(article.text)
    POLARITY = SENTIMENT_scores['compound']
    SENTIMENT = ("positive" if POLARITY > 0 else 
                 "negative" if POLARITY < 0 else 
                 "neutral")

    result['SENTIMENT'] = {
        'POLARITY': POLARITY,
        'SENTIMENT_text': SENTIMENT
    }

    return result

# URL input
url = st.text_input("Enter the url of the article/news/website you want to summarize:")

# Summarize button
if st.button("SUMMARIZE"):
    if url:
        result = summarize(url)

        # Display results with red headers
        st.markdown("<h3 style='color: #00FFFF;'>Title</h3>", unsafe_allow_html=True)
        st.write(result['title'])

        st.markdown("<h3 style='color: #00FFFF;'>Authors</h3>", unsafe_allow_html=True)
        st.write(result['authors'])

        st.markdown("<h3 style='color: #00FFFF;'>Publication Date </h3>", unsafe_allow_html=True)
        st.write(result['publication_date'])

        # Displaying the summary with proper line breaks
        st.markdown("<h3 style='color: #00FFFF;'>Summary</h3>", unsafe_allow_html=True)

        summary_lines = result['summary'].split('. ')
        formatted_summary = '<br>'.join([f"{line.strip()}." for line in summary_lines[:5]])
        st.markdown(formatted_summary, unsafe_allow_html=True)

        st.markdown("<h3 style='color: #00FFFF;'>Sentiment Analysis</h3>", unsafe_allow_html=True)
        # Display polarity and sentiment in red color
        SENTIMENT_output = f"<span style='color: #ff0000;'>POLARITY: {result['SENTIMENT']['POLARITY']}<br> SENTIMENT: {result['SENTIMENT']['SENTIMENT_text']}</span>"
        st.markdown(SENTIMENT_output, unsafe_allow_html=True)

    else:
        st.warning("please enter a url.")
