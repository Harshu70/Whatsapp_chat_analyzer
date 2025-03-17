from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
extract = URLExtract()

def fetchData(user, df):

    if user != 'Overall':
        df = df[df['user']==user]
    
    msgNum = df.shape[0]
    #no of media
    mediaNum = df[df['message']=='<Media omitted>\n'].shape[0]
    #no of words in message
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    #no of links
    link = []
    for msg in df['message']:
        link.extend(extract.find_urls(msg))
    
    return msgNum, len(words), mediaNum, len(link)

def most_active(df):
    counts = df['user'].value_counts().reset_index().rename(columns={'count':'number_of_message'})
    percentages = (df['user'].value_counts()/df.shape[0] * 100).round(2).reset_index().rename(columns={'count':'percentage_contribution'})
    
    result_df = pd.merge(counts, percentages, on='user')
    
    return result_df


def wrdCloud(user, df):
    if user != 'Overall':
        df = df[df['user']==user]

    temp_df = df[df['user']!='group_notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp_df['message'].astype(str).str.cat(sep=" "))
    return df_wc

def most_cmn_word(user, df):

    f = open('hinglish.txt', 'r')
    stop_words = f.read()

    if user != 'Overall':
        df = df[df['user']==user]

    temp_df = df[df['user']!='group_notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']

    words = []
    for msg in temp_df['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    new_df = pd.DataFrame(Counter(words).most_common(20))
    return new_df
    

def monthly(user,df):
    if user != 'Overall':
        df = df[df['user']==user]
    df['month_num'] = df['date'].dt.month
    tl = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(tl.shape[0]):
        time.append(tl['month'][i]+'-'+str(tl['year'][i]))
    tl['time'] = time
    return tl

def weekly_stat(user, df):
    if user != 'Overall':
        df = df[df['user']==user]
    df['day_name'] = df['date'].dt.day_name()
    return df['day_name'].value_counts()

def monthly_stat(user, df):
    if user != 'Overall':
        df = df[df['user']==user]
    return df['month'].value_counts()

def heatMap(user, df):
    if user != 'Overall':
        df = df[df['user']==user]
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour ==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period
    act = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return act