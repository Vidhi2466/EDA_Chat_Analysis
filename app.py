import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set page config
st.set_page_config(
    page_title="WhatsApp Analyzer",
    page_icon="💬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTitle {
        color: #25D366 !important;
        font-weight: bold;
        text-align: center;
    }
    .stHeader {
        color: #128C7E !important;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #075E54;
        padding: 1rem;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #DCF8C6;
    }
    div[data-testid="stDataFrame"] {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    div.stButton > button {
        background-color: #25D366;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #128C7E;
    }
    .stat-box {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📱 WhatsApp Analyzer")
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'system_notification' in user_list:
        user_list.remove('system_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis", key="analyze_btn"):

        # Add the analysis summary here with new styling
        st.markdown(f"""
        <div style="background-color: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 2rem;">
            <h2 style="color: #128C7E; text-align: center; font-weight: 600;"> Analysis for: <strong>{selected_user}</strong></h2>
            <div style="background-color: #e7f8e9; padding: 1.5rem; border-radius: 10px; margin-top: 1.5rem;">
                <h4 style="color: #128C7E; font-weight: 600; text-align: center; margin-bottom: 1rem;">Dashboard Features</h4>
                <ul style="color: #075E54; list-style-position: inside; padding-left: 20px;">
                    <li><strong>Top Statistics</strong>: Key metrics like total messages, words, media, and links.</li>
                    <li><strong>Timeline View</strong>: Monthly and daily message trends over time.</li>
                    <li><strong>Activity Patterns</strong>: Heatmaps showing the most active days and months.</li>
                    <li><strong>User Leaderboard</strong>: A ranking of the most active users in the chat.</li>
                    <li><strong>Content Deep Dive</strong>: A Word Cloud and analysis of the most common emojis.</li>
                    <li><strong>Sentiment Analysis</strong>: The overall emotional tone of the conversation.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats Area with enhanced styling
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("📊 Chat Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
                <div class="stat-box" style="border-left: 5px solid #25D366;">
                    <h3 style="color: #128C7E;">Total Messages</h3>
                    <h2 style="color: #25D366;">{}</h2>
                </div>
            """.format(num_messages), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class="stat-box" style="border-left: 5px solid #34B7F1;">
                    <h3 style="color: #128C7E;">Total Words</h3>
                    <h2 style="color: #34B7F1;">{}</h2>
                </div>
            """.format(words), unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class="stat-box" style="border-left: 5px solid #FF6B6B;">
                    <h3 style="color: #128C7E;">Media Shared</h3>
                    <h2 style="color: #FF6B6B;">{}</h2>
                </div>
            """.format(num_media_messages), unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
                <div class="stat-box" style="border-left: 5px solid #FFC75F;">
                    <h3 style="color: #128C7E;">Links Shared</h3>
                    <h2 style="color: #FFC75F;">{}</h2>
                </div>
            """.format(num_links), unsafe_allow_html=True)

        # monthly timeline
        st.title("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots(figsize=(10, 4))
        ax.plot(timeline['time'], timeline['message'], color='#25D366', linewidth=2.5)
        plt.xticks(rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

        # daily timeline
        st.title("📈 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black', linewidth=2.5)
        plt.xticks(rotation='vertical')
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

        # activity map
        st.title('🗓️ Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots(figsize=(10, 4))
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            ax.set_ylabel("Messages")
            ax.set_title("Busiest Days")
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            ax.set_ylabel("Messages")
            ax.set_title("Busiest Months")
            st.pyplot(fig)

        st.title("📊 Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots(figsize=(10, 6))
        ax = sns.heatmap(user_heatmap, cmap="YlGnBu")
        plt.title("Activity Heatmap")
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots(figsize=(10, 6))

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                ax.set_ylabel("Messages")
                ax.set_title("Busiest Users")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("🗣️ Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots(figsize=(8, 8))
        ax.imshow(df_wc)
        plt.axis("off")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("😊 Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots(figsize=(8, 8))
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f", colors=sns.color_palette("pastel"))
            plt.title("Top Emojis Used")
            plt.axis("equal")
            st.pyplot(fig)

        # Sentiment Analysis
        st.title("📊 Sentiment Analysis")
        
        sentiment_counts, sentiment_percentages = helper.perform_sentiment_analysis(selected_user, df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Sentiment Distribution")
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # Green for positive, Red for negative, Grey for neutral
            ax.pie(sentiment_counts, 
                  labels=sentiment_counts.index,
                  autopct='%1.1f%%',
                  colors=colors,
                  startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
            
        with col2:
            st.header("Sentiment Breakdown")
            sentiment_df = pd.DataFrame({
                'Sentiment': sentiment_percentages.index,
                'Percentage': sentiment_percentages.values
            })
            st.dataframe(sentiment_df)
    else:
        # Remove the welcome screen and keep it empty or add a minimal message
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <p style="color: #128C7E;">Select options and click 'Show Analysis' to begin</p>
            </div>
        """, unsafe_allow_html=True)
else:
    # Welcome screen with enhanced styling
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h1 style="color: #128C7E;">💬 Welcome to WhatsApp Chat Analyzer!</h1>
            <p style="color: #075E54; font-size: 1.2em;">Upload your chat file to begin the analysis journey!</p>
            <div style="background-color: #DCF8C6; padding: 1rem; border-radius: 5px; margin-top: 2rem;">
                <h4 style="color: #128C7E;">How to export your chat:</h4>
                <ol style="text-align: left; color: #075E54;">
                    <li>Open WhatsApp chat</li>
                    <li>Click on three dots ⋮</li>
                    <li>More > Export chat</li>
                    <li>Choose 'Without Media'</li>
                </ol>
            </div>
        </div>
    """, unsafe_allow_html=True)











