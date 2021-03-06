import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        consumer_key = 'XXXX'
        consumer_secret ='XXXX'
        access_token='XXXX'
        access_token_secret='XXXX'
        
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication Failed")
    
    def clean_tweet(self, tweet):
        return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",' ', tweet).split())
    
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity>0:
            return 'positive'
        elif analysis.sentiment.polarity ==0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_tweets(self, query, count =10):
        tweets =[]
        try:
            fetched_tweets = self.api.search(lang = 'english',q=query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                
                if tweet.retweet_count >0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("Error "+str(e))
                
def main():
    api = TwitterClient()
    tweets = api.get_tweets('SUV',count = 100000)
    
    pttweets = [ tweet for tweet in tweets  if tweet['sentiment']=='positive']
    print("Percentage of positive tweets : {}" .format(100*len(pttweets)/len(tweets)) )
    
    nttweets = [tweet for tweet in tweets if tweet['sentiment']=='negative']
    print("Percentage of negative tweets : {}" .format(100*len(nttweets)/len(tweets)))
    
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] =='neutral']
    ntweets_len = len(tweets) - len(pttweets) -len(nttweets)
    
    print('Percentage of neutral tweets : {}' .format(100*ntweets_len/len(tweets)))
    
    print("\nPositive tweets \n")
    for tweet in pttweets:
        print( tweet['text'])
        
    print("\n Negative tweets \n")
    for tweet in nttweets:
        print(tweet['text'])
    
    print("\n Neutral tweets \n")
    for tweet in ntweets:
        print(tweet['text'])
if __name__ =='__main__':
    main()           
