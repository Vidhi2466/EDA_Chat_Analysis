import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

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

# Helper functions
def stats_cards(num_messages, words, media, links):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-box'><p style='color:#128C7E; font-weight:bold; margin-bottom:8px; font-size:14px;'>📨 Total Messages Exchanged</p><h3 style='color:#25D366; margin-top:0; font-size:32px;'>{num_messages}</h3></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-box'><p style='color:#0088cc; font-weight:bold; margin-bottom:8px; font-size:14px;'>📝 Total Words Written</p><h3 style='color:#25D366; margin-top:0; font-size:32px;'>{words}</h3></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-box'><p style='color:#9b59b6; font-weight:bold; margin-bottom:8px; font-size:14px;'>📁 Total Media Files Shared</p><h3 style='color:#25D366; margin-top:0; font-size:32px;'>{media}</h3></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='stat-box'><p style='color:#e67e22; font-weight:bold; margin-bottom:8px; font-size:14px;'>🔗 Total Links Shared</p><h3 style='color:#25D366; margin-top:0; font-size:32px;'>{links}</h3></div>", unsafe_allow_html=True)

def plot_line(x, y, title, color="#25D366", rotation=45):
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(x, y, color=color, linewidth=2, marker='o')
    ax.set_title(title, color="#075E54", fontsize=14, fontweight='bold')
    plt.xticks(rotation=rotation)
    ax.grid(alpha=0.25)
    st.pyplot(fig)

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

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    
    st.sidebar.markdown("---")
    show_analysis = st.sidebar.button("🔍 Show Analysis", use_container_width=True, type="primary")

    if show_analysis:
        tabs = st.tabs([
            "📊 Top Statistics",
            "📈 Timeline Analysis", 
            "🗓️ Activity Patterns",
            "👥 User Leaderboard",
            "💬 Content Analysis",
            "🎭 Sentiment Analysis"
        ])

        # Tab 1: Top Statistics
        with tabs[0]:
            st.header(f"📊 Top Statistics — {selected_user}")
            st.markdown("**Get a quick overview with key metrics:**")
            
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            
            st.markdown("---")
            stats_cards(num_messages, words, num_media_messages, num_links)
            
            st.markdown("---")
            st.info("💡 These statistics provide a comprehensive overview of the chat activity including message count, word usage, media sharing, and link exchanges.")

        # Tab 2: Timeline Analysis
        with tabs[1]:
            st.header("📈 Timeline Analysis")
            st.markdown("**Visualize conversation trends over time**")
            
            st.markdown("---")
            
            st.subheader("📅 Monthly Timeline")
            st.markdown("Track message volume month by month to identify long-term trends and patterns.")
            timeline = helper.monthly_timeline(selected_user, df)
            if not timeline.empty:
                plot_line(timeline['time'], timeline['message'], "Monthly Timeline - Message Volume Over Time")
            else:
                st.warning("No monthly timeline data available.")
            
            st.markdown("---")
            
            st.subheader("📆 Daily Timeline")
            st.markdown("See the daily flow of conversation to understand day-to-day activity.")
            daily_timeline = helper.daily_timeline(selected_user, df)
            if not daily_timeline.empty:
                plot_line(daily_timeline['only_date'], daily_timeline['message'], "Daily Timeline - Day-to-Day Activity", color="#34495e", rotation=90)
            else:
                st.warning("No daily timeline data available.")

        # Tab 3: Activity Patterns
        with tabs[2]:
            st.header("🗓️ Activity Patterns")
            st.markdown("**Discover when the chat is most active**")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Most Busy Day")
                st.markdown("Bar chart highlighting the busiest days of the week.")
                busy_day = helper.week_activity_map(selected_user, df)
                if not busy_day.empty:
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(busy_day.index, busy_day.values, color='#FF6B6B', edgecolor='black', linewidth=1.2)
                    plt.xticks(rotation=45)
                    ax.set_ylabel("Number of Messages", fontweight='bold')
                    ax.set_xlabel("Day of Week", fontweight='bold')
                    ax.set_title("Most Active Days", fontweight='bold', color='#075E54')
                    ax.grid(alpha=0.3, axis='y')
                    st.pyplot(fig)
                else:
                    st.warning("No day activity data available.")
            
            with col2:
                st.subheader("📊 Most Busy Month")
                st.markdown("Bar chart highlighting the busiest months of the year.")
                busy_month = helper.month_activity_map(selected_user, df)
                if not busy_month.empty:
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(busy_month.index, busy_month.values, color='#4ECDC4', edgecolor='black', linewidth=1.2)
                    plt.xticks(rotation=45)
                    ax.set_ylabel("Number of Messages", fontweight='bold')
                    ax.set_xlabel("Month", fontweight='bold')
                    ax.set_title("Most Active Months", fontweight='bold', color='#075E54')
                    ax.grid(alpha=0.3, axis='y')
                    st.pyplot(fig)
                else:
                    st.warning("No month activity data available.")
            
            st.markdown("---")
            
            st.subheader("🔥 Activity Heatmap")
            st.markdown("A weekly heatmap showing the most active day/time combinations.")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            if user_heatmap is not None and not user_heatmap.empty:
                fig, ax = plt.subplots(figsize=(14, 7))
                sns.heatmap(user_heatmap, cmap="YlGnBu", ax=ax, linewidths=0.5, annot=True, fmt='g', cbar_kws={'label': 'Message Count'})
                ax.set_title("Activity Heatmap - Day vs Hour", fontweight='bold', fontsize=16, color='#075E54')
                ax.set_xlabel("Hour of Day", fontweight='bold')
                ax.set_ylabel("Day of Week", fontweight='bold')
                st.pyplot(fig)
            else:
                st.warning("No heatmap data available.")

        # Tab 4: User Leaderboard
        with tabs[3]:
            st.header("👥 User Leaderboard")
            st.markdown("**For group chats, see who the most active participants are**")
            
            if selected_user == "Overall":
                x, new_df = helper.most_busy_users(df)
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Top Users by Message Count")
                    st.markdown("A bar chart of the top users by message count.")
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.bar(x.index, x.values, color='#25D366', edgecolor='black', linewidth=1.2)
                    plt.xticks(rotation=45, ha='right')
                    ax.set_ylabel("Number of Messages", fontweight='bold')
                    ax.set_xlabel("Users", fontweight='bold')
                    ax.set_title("Most Active Users", fontweight='bold', color='#075E54')
                    ax.grid(alpha=0.3, axis='y')
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("📋 User Contribution Table")
                    st.markdown("A data table showing the percentage contribution of each user.")
                    st.dataframe(new_df, use_container_width=True)
                
                st.markdown("---")
                st.info("💡 This analysis helps identify the most engaged participants in the group conversation.")
            else:
                st.info("⚠️ Switch to 'Overall' to see the user leaderboard for the entire group chat.")

        # Tab 5: Content Analysis
        with tabs[4]:
            st.header("💬 Content Analysis")
            st.markdown("**Understand what is being talked about**")
            
            st.markdown("---")
            
            st.subheader("☁️ Word Cloud")
            st.markdown("A visual representation of the most frequently used words (with support for Hinglish stop words).")
            df_wc = helper.create_wordcloud(selected_user, df)
            if df_wc is not None:
                fig, ax = plt.subplots(figsize=(12, 7))
                ax.imshow(df_wc, interpolation='bilinear')
                ax.axis("off")
                ax.set_title("Most Frequently Used Words", fontweight='bold', fontsize=16, color='#075E54', pad=20)
                st.pyplot(fig)
            else:
                st.warning("No word cloud data available.")
            
            st.markdown("---")
            
            st.subheader("😊 Emoji Analysis")
            st.markdown("See the most used emojis and their distribution in a pie chart.")
            emoji_df = helper.emoji_helper(selected_user, df)
            if not emoji_df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Top Emojis Used**")
                    st.dataframe(emoji_df.head(15), use_container_width=True)
                
                with col2:
                    st.markdown("**Emoji Distribution**")
                    fig, ax = plt.subplots(figsize=(7, 7))
                    colors = sns.color_palette("pastel")
                    ax.pie(
                        emoji_df[1].head(10), 
                        labels=emoji_df[0].head(10), 
                        autopct="%0.1f%%", 
                        colors=colors,
                        startangle=90,
                        textprops={'fontsize': 10, 'fontweight': 'bold'}
                    )
                    ax.set_title("Top 10 Emojis Distribution", fontweight='bold', fontsize=14, color='#075E54')
                    st.pyplot(fig)
                
                st.markdown("---")
                st.info("💡 Emoji usage reveals the emotional tone and expressiveness of the conversation.")
            else:
                st.info("😔 No emojis found in the selected chat.")

        # Tab 6: Sentiment Analysis
        with tabs[5]:
            st.header("🎭 Sentiment Analysis")
            st.markdown("**Gauge the emotional tone of the conversation**")
            
            st.markdown("---")
            
            sentiment_counts, sentiment_percentages = helper.perform_sentiment_analysis(selected_user, df)
            
            if sentiment_counts.sum() > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Sentiment Distribution")
                    st.markdown("A pie chart showing the distribution of Positive, Negative, and Neutral messages.")
                    fig, ax = plt.subplots(figsize=(7, 7))
                    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
                    explode = tuple([0.05] * len(sentiment_counts))
                    ax.pie(
                        sentiment_counts, 
                        labels=sentiment_counts.index, 
                        autopct='%1.1f%%', 
                        colors=colors[:len(sentiment_counts)], 
                        startangle=90,
                        explode=explode,
                        shadow=True,
                        textprops={'fontsize': 12, 'fontweight': 'bold'}
                    )
                    ax.set_title("Overall Sentiment Distribution", fontweight='bold', fontsize=14, color='#075E54')
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("📋 Sentiment Breakdown")
                    st.markdown("A data table with the exact percentage breakdown.")
                    sentiment_df = sentiment_percentages.reset_index()
                    sentiment_df.columns = ['Sentiment', 'Percentage (%)']
                    sentiment_df['Percentage (%)'] = sentiment_df['Percentage (%)'].round(2)
                    
                    emoji_map = {'Positive': '😊', 'Negative': '😞', 'Neutral': '😐'}
                    sentiment_df['Emoji'] = sentiment_df['Sentiment'].map(emoji_map)
                    sentiment_df = sentiment_df[['Emoji', 'Sentiment', 'Percentage (%)']]
                    
                    st.dataframe(sentiment_df, use_container_width=True, hide_index=True)
                    
                    st.markdown("**Total Messages Analyzed:**")
                    st.markdown(f"<h3 style='color:#25D366'>{sentiment_counts.sum()}</h3>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.info("💡 Sentiment analysis uses natural language processing to classify messages as Positive, Negative, or Neutral, helping you understand the overall mood of the conversation.")
            else:
                st.warning("⚠️ No sentiment data available for analysis.")
    else:
        st.info("👆 Please click the 'Show Analysis' button in the sidebar to view the analysis.")

else:
    st.markdown("""
        <div style="text-align: center; padding: 3rem; background-color: white; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 2rem;">
            <h1 style="color: #128C7E; font-size: 2.5rem;">💬 Welcome to WhatsApp Chat Analyzer!</h1>
            <p style="color: #075E54; font-size: 1.3em; margin-top: 1rem;">Upload your chat file to begin the analysis journey!</p>
            <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); padding: 2rem; border-radius: 10px; margin-top: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                <h4 style="color: #128C7E; margin-bottom: 1rem;">📱 How to export your chat:</h4>
                <ol style="text-align: left; color: #075E54; font-size: 1.1em; line-height: 2;">
                    <li>Open WhatsApp chat</li>
                    <li>Click on three dots ⋮</li>
                    <li>More > Export chat</li>
                    <li>Choose 'Without Media'</li>
                </ol>
            </div>
        </div>
    """, unsafe_allow_html=True)











