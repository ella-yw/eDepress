def retrieve(ig_username, tw_username):
    
    def instagram(ig_username):
        
        import requests, json, urllib.request, bs4, datetime, os, csv
    
        class InstagramScraper:
        
            def __init__(self, url, user_agents=None, proxy=None): self.url = url; self.proxy = proxy
        
            def __request_url(self):
                try:
                    response = requests.get(self.url, headers={'User-Agent': 'Chrome/65.0.3325.181'})
                    response.raise_for_status()
                except requests.HTTPError: raise requests.HTTPError('Received non 200 status code from Instagram')
                except requests.RequestException: raise requests.RequestException
                else: return response.text
        
            @staticmethod
            def extract_json(html):
                body = bs4.BeautifulSoup(html, 'html.parser').find('body')
                raw_string = body.find('script').text.strip().replace('window._sharedData =', '').replace(';', '')
                return json.loads(raw_string)
        
            def page_metrics(self):
                results = {}
                try:
                    json_data = self.extract_json(self.__request_url())
                    metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
                except Exception as e: raise e
                else:
                    for key, value in metrics.items():
                        if key != 'edge_owner_to_timeline_media':
                            if value and isinstance(value, dict): results[key] = value['count']
                            elif value: results[key] = value
                return results
        
            def post_metrics(self):
                results = []
                try:
                    json_data = self.extract_json(self.__request_url())
                    metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
                except Exception as e: raise e
                else:
                    for node in metrics:
                        node = node.get('node')
                        if node and isinstance(node, dict): results.append(node)
                return results
            
        #print("\nExtracting Instagram Data From API...")
        data = InstagramScraper('https://www.instagram.com/'+ig_username+'/?hl=en').post_metrics()
        #print("Saving Instagram Data Into Directory...")
        
        if not os.path.exists("ig"): os.mkdir("ig")
        else: open("ig/ig_data.csv", "w")
        
        for ig_post in data:
            
            with open("ig/ig_data.csv", "a+", newline="", encoding="utf-8") as ig_data:
                csv.writer(ig_data).writerow([ig_post['id'], 
                                              datetime.datetime.fromtimestamp(ig_post['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                                              ig_post['edge_media_to_caption']['edges'][0]['node']['text'] if ig_post['edge_media_to_caption']['edges'] != [] else "",
                                              True])
            
            if bool(ig_post['is_video']):
                urllib.request.urlretrieve(json.loads(requests.get('https://www.instagram.com/p/' + ig_post['shortcode'] + '/?__a=1').text,
                                          )["graphql"]["shortcode_media"]["video_url"], "ig/" + str(ig_post['id']) + ".mp4")
            else: urllib.request.urlretrieve(ig_post['display_url'], "ig/" + str(ig_post['id']) + ".jpg")
        
        #print("\n")

    def twitter(tw_username):
    
        import tweepy, wget, time, json, os, csv
        
        api_key = 'noY60ockEQUfjFdz1fS3b7ZeB'
        api_secret_key = 'itE8jzxQ8BXDmh4Le61m4fHgM90X3IfK1pf7URGQmxEOuYi6si'
        access_token = '4316836098-ef4Nwfg8g49DSbFdcn7B2DpEXaMo9TBJAuqp3ya'
        access_token_secret = '4E6ARa8DKqJktJ5rE0MakJ3u4Eg47gWovYIeajOyUgghm'
        
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        
        #print("Extracting Twitter Data From API...")
        data = tweepy.API(auth).user_timeline(screen_name = tw_username, count = 12, tweet_mode='extended')
        #print("Saving Twitter Data Into Directory...")
        
        if not os.path.exists("tw"): os.mkdir("tw")
        else: open("tw/tw_data.csv", "w")
        
        for tw_post in data:
            
            media_post = tw_post.entities.get('media', [])
            
            tw_post = json.loads(json.dumps(tw_post._json))
            
            media = False
            if(len(media_post) > 0): 
                wget.download(media_post[0]['media_url'], out = "tw/" + str(tw_post['id']) + "." + media_post[0]['media_url'].split(".")[-1])
                media = True
                
            with open("tw/tw_data.csv", "a+", newline="", encoding="utf-8") as tw_data:
                csv.writer(tw_data).writerow([tw_post['id'], 
                                              time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tw_post['created_at'], '%a %b %d %H:%M:%S +0000 %Y')),
                                              tw_post['full_text'],
                                              media])     
        #print("\n")
    
    """
    def facebook(fb_username):
        
        import facebook, urllib.request, requests, html2text, os, csv
        
        access_token = "EAAAAAYsX7TsBABZCZArGdn6FmaWSuoEBuypMvoIGphuIBGZBaTDWuyunS1lzP1Ad5cbtk2MJOv9d95no1QUmtdkei4A6ZAUPbBLo7nfwZA8vC5SYHUAGDdgZAr2sIUKNjUX2A1OfTLnBBvFQcEO9sMeLzP7R8IGNUIzDJyVEjvJZCYtp1ZC5NZAAx7iXxwt1sNuDZBFfovkZAZBMK7umIa5izAZBQo74pT0j9yXwZD"
        
        #print("Extracting Facebook Data From API...")
        data = facebook.GraphAPI(access_token).get_object(id = fb_username, 
               fields = 'id,posts.with(<value>){type,created_time,full_picture,link,source,message}')['posts']['data']
        #print("Saving Facebook Data Into Directory...")
        
        if not os.path.exists("fb"): os.mkdir("fb")
        else: open("fb/fb_data.csv", "w")
        
        for fb_post in data[:12]:
            
            media = True
            if fb_post['type'] == "photo": urllib.request.urlretrieve(fb_post['full_picture'], "fb/" + str(fb_post['id']) + ".jpg")
            elif fb_post['type'] == "video": urllib.request.urlretrieve(fb_post['source'], "fb/" + str(fb_post['id']) + ".mp4")
            elif fb_post['type'] == "link": 
                h = html2text.HTML2Text(); h.ignore_links = True
                open("fb/" + str(fb_post['id']) + ".txt", "a", encoding="utf-8").write(h.handle(requests.get(fb_post['link']).text))
            else: media = False
                
            with open("fb/fb_data.csv", "a+", newline="", encoding="utf-8") as fb_data:
                try: msg = fb_post['message']
                except KeyError: msg = ''
                csv.writer(fb_data).writerow([fb_post['id'], 
                                              fb_post['created_time'].replace("T", " ").split("+")[0],
                                              msg,
                                              media])
        #print("\n")
    """
    
    def main():
    
        if ig_username != "": instagram(ig_username)
        if tw_username != "": twitter(tw_username)
        #if fb_username != "": facebook(fb_username)
        
    main()