# 💬 WhatsApp Chat Analyzer

A powerful and feature-rich web application built with Streamlit to analyze and visualize your WhatsApp chats. Upload your exported chat file and get instant insights into messaging patterns, user activity, content trends, and emotional sentiment.

 <!-- It's highly recommended to replace this with a real screenshot of your app! -->

---

## ✨ Features

This dashboard provides a deep dive into your WhatsApp conversations with the following analytical features:

-   **Top Statistics**: Get a quick overview with key metrics:
    -   Total Messages Exchanged
    -   Total Words Written
    -   Total Media Files Shared
    -   Total Links Shared
-   **Timeline Analysis**: Visualize conversation trends over time.
    -   **Monthly Timeline**: Track message volume month by month.
    -   **Daily Timeline**: See the daily flow of conversation.
-   **Activity Patterns**: Discover when the chat is most active.
    -   **Activity Heatmap**: A weekly heatmap showing the most active day/time combinations.
    -   **Most Busy Day & Month**: Bar charts highlighting the busiest days of the week and months of the year.
-   **User Leaderboard**: For group chats, see who the most active participants are.
    -   A bar chart of the top users by message count.
    -   A data table showing the percentage contribution of each user.
-   **Content Analysis**: Understand what is being talked about.
    -   **Word Cloud**: A visual representation of the most frequently used words (with support for Hinglish stop words).
    -   **Emoji Analysis**: See the most used emojis and their distribution in a pie chart.
-   **Sentiment Analysis**: Gauge the emotional tone of the conversation.
    -   A pie chart showing the distribution of **Positive**, **Negative**, and **Neutral** messages.
    -   A data table with the exact percentage breakdown.

---

## 🚀 How to Run Locally

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### 2. Create a Virtual Environment (Recommended)

It's a good practice to create a virtual environment to keep project dependencies isolated.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

Once the dependencies are installed, run the following command in your terminal to start the application:

```bash
streamlit run app.py
```

Your web browser should automatically open to the application's URL (usually `http://localhost:8501`).

---

## 📲 How to Export Your WhatsApp Chat

To get a chat file for analysis, follow these steps in WhatsApp:

1.  Open the individual or group chat you want to analyze.
2.  Tap on the three dots (**⋮**) in the top-right corner.
3.  Tap on **More** > **Export chat**.
4.  Choose **Without Media**.
5.  Save or send the exported `.txt` file to your computer.

---

## 🛠️ Technologies Used

-   **Streamlit**: For building the interactive web application.
-   **Pandas**: For data manipulation and analysis.
-   **Matplotlib & Seaborn**: For creating static and interactive visualizations.
-   **WordCloud**: For generating word cloud images.
-   **TextBlob**: For performing simple sentiment analysis.
-   **Emoji**: For handling and analyzing emojis in the text.
-   **URLExtract**: For finding and extracting URLs from messages.

---

## 📂 Project Structure

```
.
├── app.py              # Main Streamlit application script
├── helper.py           # Core analysis functions
├── preprocessor.py     # Data cleaning and preprocessing script
├── requirements.txt    # List of Python dependencies
├── stop_hinglish.txt   # Custom stop words for text analysis
└── README.md           # This file
```