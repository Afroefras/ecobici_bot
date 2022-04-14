from map import EcoBiciMap
from os import environ

ECOBICI_CLIENT_ID = environ['ECOBICI_CLIENT_ID']
ECOBICI_CLIENT_SECRET = environ['ECOBICI_CLIENT_SECRET']
# ECOBICI_CLIENT_ID = '2199_132ley5lk3404wkk4c4w4ggo48kwcokosogg0k0www84s08gs'
# ECOBICI_CLIENT_SECRET = '61xytd2ketssok44g4kkckwogkg048gk0ok48sc0k0wgc8scs'

if __name__ == "__main__":
    ebm = EcoBiciMap(ECOBICI_CLIENT_ID, ECOBICI_CLIENT_SECRET)
    ebm.get_map(color='#1B1B1B', edgecolor='#00acee', points_palette='Blues')