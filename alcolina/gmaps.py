import googlemaps
from .settings import settings
from . import models

DISTANCE = 1000

gmaps = googlemaps.Client(key=settings.GOOGLEMAPS_API_KEY)


def get_gas_stations(loc: models.gmaps.Location, radius=DISTANCE):
    ret = []
    next_page_token = None

    print('API_CALL: ', next_page_token)
    res = gmaps.places_nearby(
        location=loc.set,
        keyword='gas station',
        # radius=radius,
        rank_by='distance',
        page_token=next_page_token,
        type='gas_station',
        # name='gas station'
    )
    next_page_token = res.get('next_page_token', '')
    for g in res.get('results'):
        yield models.gas_station.GasStation.parse_obj(g)

    #return [GasStation.parse_obj(r) for r in res.get('results')].pop(-1)

def get_gas_station_prices(gas_station: models.gas_station.GasStation) -> models.gas_station.GasStation:
    print(gas_station.place_id)
    return

def set_gas_station_prices(prices: models.gas_station.Prices) -> models.gas_station.Prices:
    print(prices.json())

    return
