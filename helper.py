from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import TextBlob
import numpy as np

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # fetch number of messages
    num_messages = df.shape[0]
    
    # fetch total words
    words = []
    for message in df['message']:
        if pd.notna(message):  # Check for NaN values
            words.extend(str(message).split())
    
    # Count media messages - looking for the exact patterns in your chat
    media_count = 0
    for message in df['message']:
        if pd.notna(message):
            # Clean the message of invisible characters and convert to lowercase
            clean_msg = str(message).replace('\u200e', '').replace('\u200f', '').strip().lower()
            
            # Check for media patterns exactly as they appear in your chat
            if (clean_msg == 'image omitted' or 
                clean_msg == 'video omitted' or 
                clean_msg == 'document omitted' or
                clean_msg == 'sticker omitted' or
                clean_msg == 'gif omitted' or
                clean_msg == 'audio omitted' or
                'document omitted' in clean_msg):
                media_count += 1
    
    # fetch number of links shared
    links = []
    for message in df['message']:
        if pd.notna(message):
            links.extend(extract.find_urls(str(message)))
    
    return num_messages, len(words), media_count, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index()
    new_df.columns = ['name', 'percent']
    return x, new_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out media messages properly
    temp = df[~df['message'].str.contains('omitted', case=False, na=False)]
    if temp.empty:
        temp = df  # fallback if no messages left
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    try:
        # Fixed file reference
        with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
            stop_words = set(f.read().splitlines())
    except FileNotFoundError:
        stop_words = {'aap', 'aur', 'ka', 'ki', 'ko', 'hai', 'he', 'ye', 'to', 'kya', 'me', 'se', 'ne', 'par'}
    
    if selected_user != 'Overall':
        df = df[selected_user == df['user']]
    
    # Filter out media messages properly
    temp = df[~df['message'].str.contains('omitted', case=False, na=False)]
    words = []
    
    for message in temp['message']:
        if pd.notna(message):
            for word in str(message).lower().split():
                if word not in stop_words and len(word) > 1:
                    words.append(word)
    
    word_freq = pd.DataFrame(Counter(words).most_common(20))
    if not word_freq.empty:
        word_freq.columns = ['Word', 'Frequency']
    
    return word_freq

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        if pd.notna(message):
            emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])
    
    if emojis:
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return emoji_df
    else:
        return pd.DataFrame()

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    activity_heatmap = df.pivot_table(index='day_name', columns='period', 
                                    values='message', aggfunc='count').fillna(0)
    return activity_heatmap

def perform_sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out media messages and system notifications properly
    df = df[~df['message'].str.contains('omitted', case=False, na=False)]
    df = df[df['user'] != 'system_notification']
    
    if df.empty:
        return pd.Series(), pd.Series()
    
    # Calculate sentiment for each message
    sentiments = []
    for message in df['message']:
        if pd.notna(message) and len(str(message).strip()) > 0:
            blob = TextBlob(str(message))
            sentiment = blob.sentiment.polarity
            if sentiment > 0:
                sentiments.append('Positive')
            elif sentiment < 0:
                sentiments.append('Negative')
            else:
                sentiments.append('Neutral')
    
    if not sentiments:
        return pd.Series(), pd.Series()
    
    # Create sentiment DataFrame
    sentiment_df = pd.DataFrame({'Sentiment': sentiments})
    
    # Calculate percentages
    sentiment_counts = sentiment_df['Sentiment'].value_counts()
    sentiment_percentages = (sentiment_counts / len(sentiment_df) * 100).round(2)
    
    return sentiment_counts, sentiment_percentages

def debug_media_messages(df):
    """Debug function to see what media messages look like"""
    print("=== DEBUG: All unique messages ===")
    unique_messages = df['message'].unique()[:20]  # First 20 unique messages
    for i, msg in enumerate(unique_messages):
        print(f"{i+1}: '{msg}'")
    
    print("\n=== DEBUG: Media candidates ===")
    media_candidates = []
    
    for msg in df['message'].unique():
        if pd.notna(msg):
            msg_str = str(msg).lower()
            if 'omitted' in msg_str or 'media' in msg_str or 'image' in msg_str:
                media_candidates.append(msg)
    
    for i, msg in enumerate(media_candidates):
        print(f"{i+1}: '{msg}'")
    
    return media_candidates















