import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import json
import csv

def percentage(part, whole):
    return 100 * float(part) / float(whole)

consumerKey = ""
consumerSecret = ""
accessKey = ""
accessTokenSecret = ""
#hashtag = input("Enter hashtag or content of interest: ")
hashtag = "freesowore"
#noOfSearches = int(input("Enter the number of searches to be made aka sample population: "))
noOfSearches = 50

def search_hashtag(c_k, c_s, a_k, a_s, h, n):
    #creating authentication 
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    
    #initialize api
    api = tweepy.API(auth)
    
    #taking pole
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0    

    
    #name the spreadsheet
    name = '_'.join(re.findall(r"#(\w+)", h))
    #opening the spreadsheet
    with open('%s.csv'%(name), 'wb') as f:
        w = csv.writer(f)
        #write header row to spreadsheet
        w.writerow(['Timestamp', 'Tweet', 'username', 'all_hashtags', 'No_of_followers'])
        
        tweets = tweepy.Cursor(api.search, q= h + '-filter:retweets', lang = "English", tweet_mode = 'extended').items(n)
        for tweet in tweets:
            w.writerow([tweet.created_at, tweet.full_text.replace('\n', ' ').encode('utf-8'),
                        tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet.json['entities']['hashtags']], tweet.user.followers_count])
       
            analysis  = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity
            if (polarity == 0):
                neutral += 1
            elif (polarity > 0.00):
                positive += 1
            elif (polarity < 0.00):
                negative += 1
    positive = format(percentage(positive, noOfSearches),'.2f')
    negative = format(percentage(negative, noOfSearches), '.2f')
    neutral = format(percentage(neutral, noOfSearches), '.2f')
                
    print("People's response to ", h , "by analyzing " , n , "tweets." )
    if polarity == 0:
        print('neutral')
    elif polarity > 0:
        print('positive')
    elif polarity < 0:
        print('negative')
        
    labels = ['positive[' + str(positive) + '%]', 'neutral[' + str(neutral) +'%]', 'negative[' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'gold', 'red']
    patches, text = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches) 
    plt.title("People's reaction to " + h + " by analyzing "+ n + "tweets")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    
search_hashtag(consumerKey, consumerSecret, accessKey, accessTokenSecret, hashtag, noOfSearches)