# BASIC TWITTER MONITOR (UNFILTERED TWEETS)
# MADE BY github.com/rTunaboss

# # # # # # # # # # # # # # # # # # # #     IMPORTS        # # # # # # # # # # # # # # # # # # # #
import tweepy
from dhooks import Webhook, Embed
import random
import json
from pyfiglet import figlet_format



# # # # # # # # # # # # # # # # # # # #     TODO USER SETUP        # # # # # # # # # # # # # # # # # # # #
#Enter your discord webhook here
MONITOR_WEBHOOK = ""
USER_IDS = [
    "929793229725110272",   #rTUNAboss
]
#Don't forget to setup your credentials in credentials.json


# # # # # # # # # # # # # # # # # # # #     VARIABLES        # # # # # # # # # # # # # # # # # # # #
with open("credentials.json", "r") as f:
    credentials = json.loads(f.read())
CONSUMER_KEY = credentials['CONSUMER_KEY']
CONSUMER_SECRET = credentials['CONSUMER_SECRET']
ACCESS_TOKEN = credentials['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']

#Hex list for webhook colors
HEX_LIST = [
    16725342,
    16604024,
    16736311,
]


class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        j = json.loads(data)
        if "delete" not in j:
            tweet_content = get_tweet_content(j)
            user = get_user(j)
            tweet_url = get_tweet_url(j)
            profile_pic_url = get_profile_pic(j)
            screen_name = get_screen_name(j)
            notify_twitter(
                webhook_url=MONITOR_WEBHOOK,
                tweet_content=tweet_content,
                user=user,
                tweet_url=tweet_url,
                profile_pic=profile_pic_url,
                screen_name=screen_name,
                )



#####   JSON EXTRACTING FUNCTIONS    #####
def get_tweet_url(j):
    '''Takes in json file with tweet data and returns a tweet url'''
    return f"https://twitter.com/{j['user']['screen_name']}/status/{j['id']}"
def get_profile_pic(j):
    '''Takes in json file and returns an URL of users profile picture'''
    return j["user"]["profile_image_url"]
def get_tweet_content(j):
    '''Takes in json file and returns tweet contents'''
    return j['text']
def get_screen_name(j):
    '''Takes in json file and returns users screen name'''
    return j['user']['screen_name']
def get_user_url(j):
    '''Takes in json of tweet data and returns URL provided in users BIO'''
    return j['user']['url']
def get_user(j):
    return j["user"]["name"]


#####   WEBHOOK FUNCTIONS    #####
def notify_twitter(webhook_url, tweet_content, user,tweet_url, profile_pic, screen_name):
    '''Sends Embed to the TwitterMonitor'''
    hook = Webhook(url=webhook_url)
    color= random.choice(HEX_LIST)

    embed = Embed(
        title = f"New tweet from {user}",
        url = tweet_url,
        color=color,
        timestamp = 'now',
        description = tweet_content,
    )

    embed.set_author(name=screen_name,icon_url=profile_pic,url=f'https://twitter.com/{screen_name}')
    embed.set_footer(text='rTUNAboss TwitterMonitor', icon_url="https://scontent-frx5-1.cdninstagram.com/vp/aadc24b1c711307a28abcb5c2b8f4c16/5DCC61B6/t51.2885-19/s320x320/64845864_325154095079310_267583884244287488_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com")

    hook.send(embed=embed)

# # # # # # # # # # # # # # # # # # # #     RUNNING THE CODE        # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    print(figlet_format(('rTunaboss'), font='big'))

    listener = StreamListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = tweepy.Stream(auth, listener)

    stream.filter(follow=USER_IDS, is_async=True)