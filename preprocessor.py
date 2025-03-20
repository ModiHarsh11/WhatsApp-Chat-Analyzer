import re
import pandas as pd
def preprocess(data):

    # Define regular expression patterns
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Compile regular expression patterns
   # regex_12_hour = re.compile(pattern_12_hour)
    #regex_24_hour = re.compile(pattern_24_hour)

    # Apply both patterns to the sample data
   # matches = []

    # Loop through each line in the sample data
   # for line in data.split('\n'):
        # Check for matches with 12-hour pattern
    #    match_12_hour = regex_12_hour.search(line)
     #   if match_12_hour:
      #      matches.append(match_12_hour.group())

        # Check for matches with 24-hour pattern
       # match_24_hour = regex_24_hour.search(line)
       # if match_24_hour:
        #    matches.append(match_24_hour.group())

    # Print the matches
    #print(matches)

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    # Assuming 'messages' and 'dates' are defined elsewhere in your code
    # Ensure they contain the expected data

    # Create DataFrame from messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert 'message_date' type to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

    # Rename 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['date_num'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df