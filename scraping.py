import snscrape.modules.twitter as sntwitter
import pandas as pd


query = "(from:elonmusk) until:2023-01-01 since:2022-10-01"
tweets = []
limit = 1000

# to show all th data 

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
     print(vars(tweet))

#to show column wise data

query = "(from:elonmusk) until:2023-01-01 since:2022-10-01"
tweets = []
limit = 1000


for tweet in sntwitter.TwitterHashtagScraper(query).get_items():
    
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.url, tweet.user.username, tweet.sourceLabel, tweet.user.location, tweet.rawContent, tweet.likeCount, tweet.retweetCount,  tweet.quoteCount, tweet.replyCount])
        
df = pd.DataFrame(tweets, columns=['Date', 'TweetURL','User', 'Source', 'Location', 'Tweet', 'Likes_Count','Retweet_Count', 'Quote_Count', 'Reply_Count'])

print(df)


# to convert in to csv file

df.to_csv('tweets.csv')