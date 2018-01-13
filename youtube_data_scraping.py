## Youtube Data Scraping


from urllib.request import urlopen
import json
import pafy
import pandas as pd





from google_auth import api_key


# In[3]:


def get_all_video_in_channel(channel_id):
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)

    video_links = []
    url = first_url
    while True:
        inp = urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links


# In[4]:


channel_id = "UClzR7HySZTVb6g-tSzAhi5A"


# In[5]:


video_urls = get_all_video_in_channel(channel_id)


# In[6]:


from multiprocessing import Pool
p=Pool(10)


# In[7]:


#getvideo(video_urls)


# In[8]:


results = []

for url in video_urls: 
    test = pafy.new(url)
    result = test.published,test.title, test.rating, test.viewcount, test.duration, test.likes, url
    results.append(result)
    print(test.title)


# In[9]:


print("The link to the first video is: " + results[-1][-1])
print("The link to the most recent video is: " + results[0][-1])


# In[10]:


df = pd.DataFrame(results, columns = ["Date", "Title", "Rating", "View Count", "Duration", "Likes", "URL"])
df.head()


# In[11]:


df.tail()


# In[12]:


least_viewed = df.sort_values(by='View Count')
least_viewed.head()


# In[13]:


least_viewed_url = least_viewed.iloc[0, 6]
least_view_title = least_viewed.iloc[0,1]
print("The video with the fewest views is '{}' and it's link is: {}.".format(least_view_title, least_viewed_url))


# In[14]:


message = "Learning #Chinese ? Me too! Check out my video '{}' here: {}".format(least_view_title, least_viewed_url)
print(message)


# In[15]:


from twython import Twython
from twitter_auth import (
    consumer_key, 
    consumer_secret,
    access_token, 
    access_token_secret
)


# In[16]:


twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)


# In[17]:


twitter.update_status(status=message)

