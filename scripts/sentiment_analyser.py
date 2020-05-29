import re
import pandas
import swifter
from textblob import TextBlob
import numpy as np

def do_analysis(text):
    global iterator
    global total
    iterator += 1
    print(str(iterator) + " / " + str(total))
    try:
        analysis = TextBlob(clean_text(text))
        return analysis.sentiment.polarity
    except:
        return "0"


def clean_text(text):
    # Remove links, special characters

    return  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", text).split())

    # import files into df


# run function on each row into a new column
# save into csv

parse_dates = ['timestamp']

iterator = 0
#
fields = ['timestamp', 'text']

#
df = pandas.read_csv('reddit_bitcoin_raw.csv', dtype={"timestamp": str, "text": str},
                     usecols=fields, sep='\;\;\;\;\;', parse_dates=parse_dates)
df.set_index("timestamp", inplace=True)
total = len(df.index)
df.sort_index()
df["sentiment"] = df["text"].swifter.apply(lambda x: do_analysis(str(x)))
df.drop(['text'], axis=1, inplace=True)
df.to_csv('bitcoin_sentiment.csv', sep=';', index=True)
exit(0)
fields = ['timestamp', 'sentiment']
df = pandas.read_csv('litecoin_sentiment.csv', dtype={"timestamp": int, "sentiment": float}, usecols=fields, sep=';')
df['timestamp'] = pandas.to_datetime(df['timestamp'], unit='s')
sentiment = df.groupby([df.timestamp.dt.floor("H")])['sentiment'].mean()
count = df.groupby([df.timestamp.dt.floor("H")])['sentiment'].size()
count = count.asfreq('1H')
count = count.fillna(0)
sentiment_df = pandas.concat([sentiment], axis=1)
sentiment_df = sentiment_df.asfreq('1H')
sentiment_df.ffill(inplace=True)
sentiment_df["count"] = count

df = pandas.read_csv("../reddit/ltc_total.csv", sep=",")
df.drop("index", axis=1, inplace=True)
df['date'] = pandas.to_datetime(df['date'])
df.set_index(df["date"], inplace = True)
df = df.loc[~df.index.duplicated(keep='last')]
df.drop("date", inplace = True, axis=1)
df = df.asfreq('1H')
df = df.interpolate()
df["total"] = df["total"].round()
sentiment_df = sentiment_df.join(df)
sentiment_df.dropna(inplace=True)
sentiment_df.reset_index(inplace=True)
sentiment_df["timestamp"] = (sentiment_df["timestamp"] - pandas.Timestamp("1970-01-01")) // pandas.Timedelta('1s')
sentiment_df.to_csv('litecoin_daily.csv', sep=';', index=False)

