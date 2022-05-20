from map import EcoBiciMap
from os import environ

ECOBICI_CLIENT_ID = environ['ECOBICI_CLIENT_ID']
ECOBICI_CLIENT_SECRET = environ['ECOBICI_CLIENT_SECRET']

TWITTER_CONSUMER_KEY = environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = environ['TWITTER_ACCESS_TOKEN_SECRET']


if __name__ == "__main__":
    ebm = EcoBiciMap(ECOBICI_CLIENT_ID, ECOBICI_CLIENT_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    ebm.get_map(
        shp_first_time=False, 
        padding=0.006,
        # color='#1B1B1B',
        color='#ffffff',
        edgecolor='#00acee', 
        points_palette='Blues'
    )