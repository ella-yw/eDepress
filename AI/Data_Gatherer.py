import tweepy, wget, time, json, os, csv

####################################################################    

api_key = 'noY60ockEQUfjFdz1fS3b7ZeB'
api_secret_key = 'itE8jzxQ8BXDmh4Le61m4fHgM90X3IfK1pf7URGQmxEOuYi6si'
access_token = '4316836098-ef4Nwfg8g49DSbFdcn7B2DpEXaMo9TBJAuqp3ya'
access_token_secret = '4E6ARa8DKqJktJ5rE0MakJ3u4Eg47gWovYIeajOyUgghm'
        
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
tweet = api.home_timeline()

for hashtag in ["depressed", "anxiety", "lost", "sad", "weak", "outcast", "suicidal", "miserable", "hurting", "spiritless"]:
    
    with open("Depression_Data.csv", "a+", newline="", encoding="utf-8") as tw_data:
        
        wr = csv.writer(tw_data)
        
        for tweet in tweepy.Cursor(api.search, q = hashtag + ' -filter:retweets', lang="en", tweet_mode='extended').items(200):
            
            media_post = tweet.entities.get('media', [])
            media = False
            if(len(media_post) > 0): 
                wget.download(media_post[0]['media_url'], out = "Depression Images/" + str(tweet.id) + "." + media_post[0]['media_url'].split(".")[-1])
                media = True
                
            wr.writerow([tweet.id, 
                         tweet.created_at,
                         tweet.user.screen_name,
                         tweet.full_text.replace('\n',' '),
                         [hashtag, [e['text'] for e in tweet._json['entities']['hashtags']]],
                         media])
    
####################################################################    

api_key = 'dM8Y7jGsIvAXsTfPUAbgA'
api_secret_key = '3egv0eTWNb9pqUFmu6MQPi4PGe8YY0nSZohv19SNQP4'
access_token = '16560379-pZ1npTEgcYS9yzZcONSE0WUWC2NzOLwS0f0PdToOY'
access_token_secret = 'BL3Yq9ZHOeyDfIX5rcQjZvoY4sJVy2Sw8xOfvsKl3wYmV'

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
tweet = api.home_timeline()
    
for hashtag in ["puppies", "ice cream", "water", "coder", "relaxed", "winner", "living", "god", "toronto", "journey"]:
    
    with open("Normal_Data.csv", "a+", newline="", encoding="utf-8") as tw_data:
        
        wr = csv.writer(tw_data)
        
        for tweet in tweepy.Cursor(api.search, q = hashtag + ' -filter:retweets', lang="en", tweet_mode='extended').items(200):
            
            media_post = tweet.entities.get('media', [])
            media = False
            if(len(media_post) > 0): 
                wget.download(media_post[0]['media_url'], out = "Normal Images/" + str(tweet.id) + "." + media_post[0]['media_url'].split(".")[-1])
                media = True
                
            wr.writerow([tweet.id, 
                         tweet.created_at,
                         tweet.user.screen_name,
                         tweet.full_text.replace('\n',' '),
                         [hashtag, [e['text'] for e in tweet._json['entities']['hashtags']]],
                         media])