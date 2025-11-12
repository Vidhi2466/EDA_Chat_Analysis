import re
import pandas as pd

def preprocess(data):
    # This pattern is designed to handle the invisible space (U+202F) before AM/PM
    # It also correctly captures multi-line messages.
    pattern = r'(\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s?[APM]{2}\])'
    
    # Split the data by the timestamp pattern
    messages = re.split(pattern, data)[1:]
    
    # The result is a flat list of [timestamp, message, timestamp, message, ...]
    # We group them into pairs
    dates = messages[::2]
    message_texts = messages[1::2]
    
    # Create the DataFrame
    df = pd.DataFrame({'user_message': message_texts, 'message_date': dates})
    
    # 1. Clean and convert the date column
    # Remove brackets and the invisible space before AM/PM
    df['message_date'] = df['message_date'].str.replace('[\[\]]', '', regex=True)
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=True) # Replace narrow no-break space
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p')

    # 2. Extract users and messages
    users = []
    messages = []
    for message in df['user_message']:
        # The message starts with ' User Name: message content'
        # The invisible character (U+200E) is at the start of the message content itself
        entry = re.split('([\w\W]+?):\s', message, maxsplit=1)
        
        if len(entry) > 2:  # If a user name is found
            users.append(entry[1].strip())
            # The actual message content, clean the leading invisible char and whitespace
            messages.append(entry[2].strip().lstrip('\u200e').strip())
        else:
            users.append('system_notification')
            # This is a system notification, clean it
            messages.append(entry[0].strip().lstrip('\u200e').strip())

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # 3. Extract date & time features
    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    # Create time period for heatmap
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append('23-00')
        elif hour == 0:
            period.append('00-01')
        else:
            period.append(f'{hour:02d}-{hour + 1:02d}')
    df['period'] = period

    return df

def get_message_type(message):
    if 'image omitted' in message:
        return 'image'
    elif 'video omitted' in message:
        return 'video'
    elif 'document omitted' in message:
        return 'document'
    elif 'sticker omitted' in message:
        return 'sticker'
    elif 'GIF omitted' in message:
        return 'gif'
    elif 'audio omitted' in message:
        return 'audio'
    elif message.startswith('This message was deleted'):
        return 'deleted'
    elif 'created this group' in message or 'added' in message or 'left' in message:
        return 'notification'
    else:
        return 'text'