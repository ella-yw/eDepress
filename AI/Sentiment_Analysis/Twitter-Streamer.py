from tweepy.streaming import StreamListener
from tweepy import OAuthHandler,  Stream

#Timezone on computer has to be taken automatically

consumer_key = "noY60ockEQUfjFdz1fS3b7ZeB"
consumer_secret = "itE8jzxQ8BXDmh4Le61m4fHgM90X3IfK1pf7URGQmxEOuYi6si"
access_token = "4316836098-ef4Nwfg8g49DSbFdcn7B2DpEXaMo9TBJAuqp3ya"
access_secret = "4E6ARa8DKqJktJ5rE0MakJ3u4Eg47gWovYIeajOyUgghm"

class StdOutListener(StreamListener):
    
    def on_data(self, data): 
        
        try: open('Streamed-Data.txt', 'a').write(data + '\n'); return True
        except BaseException as e: print('failed on_date ' + str(e))
            
    def on_error(self, status): print(status)

if __name__ == '__main__':

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    stream = Stream(auth, StdOutListener())
    stream.filter(track=['depression', 'anxiety', 'mental health'])