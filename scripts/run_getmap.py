from tkinter.tix import Tree
from map import EcoBiciMap
from os import environ

# ECOBICI_CLIENT_ID = environ['ECOBICI_CLIENT_ID']
# ECOBICI_CLIENT_SECRET = environ['ECOBICI_CLIENT_SECRET']

# TWITTER_CONSUMER_KEY = environ['TWITTER_CONSUMER_KEY']
# TWITTER_CONSUMER_SECRET = environ['TWITTER_CONSUMER_SECRET']
# TWITTER_ACCESS_TOKEN = environ['TWITTER_ACCESS_TOKEN']
# TWITTER_ACCESS_TOKEN_SECRET = environ['TWITTER_ACCESS_TOKEN_SECRET']

ECOBICI_CLIENT_ID = '2199_132ley5lk3404wkk4c4w4ggo48kwcokosogg0k0www84s08gs'
ECOBICI_CLIENT_SECRET = '61xytd2ketssok44g4kkckwogkg048gk0ok48sc0k0wgc8scs'

TWITTER_CONSUMER_KEY = 'LekadufpFPEcpu2n5arDEqfz8'
TWITTER_CONSUMER_SECRET = 'po3kkAn88rTMK8aoVG65oOLgInflEdWtTmlZEK04BUy7RfDClA'

TWITTER_ACCESS_TOKEN = '1495092461739200513-6wyjGzuLAvuBzJ4DPDOsw2MCQKV2kE'
TWITTER_ACCESS_TOKEN_SECRET = '8hmwtPNa7flSxN1QpO6mJsi3ndBBMofwWKcmfSy1EYw7o'


if __name__ == "__main__":
    ebm = EcoBiciMap(ECOBICI_CLIENT_ID, ECOBICI_CLIENT_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, is_local=True)
    ebm.get_map(
        img_name='future_map',
        shp_first_time=False, 
        padding=0.006,
        # color='#1B1B1B',
        color='#ffffff',
        edgecolor='#00acee', 
        points_palette='Blues'
    )