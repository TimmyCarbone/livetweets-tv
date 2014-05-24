import os
from twython import Twython

APP_KEY               = os.environ['TVLIVETWEETS_TW_KEY']
APP_SECRET            = os.environ['TVLIVETWEETS_TW_SECRET']

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)

ACCESS_TOKEN          = twitter.obtain_access_token()
ACCESS_TOKEN_SECRET   = os.environ['TVLIVETWEETS_TW_TOKEN_SECRET']

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)