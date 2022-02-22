from map import EcoBiciMap
from os import environ

ECOBICI_CLIENT_ID = environ['ECOBICI_CLIENT_ID']
ECOBICI_CLIENT_SECRET = environ['ECOBICI_CLIENT_SECRET']

if __name__ == "__main__":
    ebm = EcoBiciMap(ECOBICI_CLIENT_ID, ECOBICI_CLIENT_SECRET)
    ebm.get_map(color='#1B1B1B', edgecolor='#00acee', points_palette='Blues')