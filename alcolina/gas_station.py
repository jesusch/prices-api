import json
from fastapi import APIRouter, Depends


from .aws import s3_res
from . import auth, gmaps, models
from .settings import settings


router = APIRouter(prefix='/gas_station', tags=['gas_station'])


@router.get('/')
def get_gas_stations(lat: float = -23.597046, lng: float = -46.6526055, current_user: auth.User = Depends(auth.get_current_active_user)):
    loc = models.gmaps.ReverseLocation.reverse_geocode(lat,lng)
    if loc.country.short_name != 'BR':
        return # TODO

    for station in gmaps.get_gas_stations(loc.location):
        print(station.distance(loc.location))
    #print(list(stations))

    return loc

    # loc = models.gmaps.Location(lat=lat, lng=lng)
    # ret = []
    # for g in gmaps.get_gas_stations(loc):
    #     ret.append(g)
    #     print(models.gas_station.reverse(lat,lng))
    # return ret
    gas_station = GasStation(place_id=place_id)
    try:
        gas_station.get_prices()
    except:
        return gas_station

@router.get('/pbras/prices')
async def get_pbras_prices(current_user: auth.User = Depends(auth.get_current_active_user)) -> dict:
    pbras_prices = s3_res.Object(settings.BUCKET, 'prices/pbras.prices.json')
    return json.load(pbras_prices.get().get('Body'))

@router.get('/{place_id}/price')
def get_gas_station_price(place_id: str, current_user: auth.User = Depends(auth.get_current_active_user)):
    gas_station = models.gas_station.GasStation(place_id=place_id)
    try:
        gas_station.get_prices()
    except:
        return gas_station


@router.post('/{place_id}/price')
def set_gas_station_price(place_id: str, item: models.gas_station.Prices, current_user: auth.User = Depends(auth.get_current_active_user)):

    prices = models.gas_station.Prices.parse_obj(item)
    gas_station = models.gas_station.GasStation(place_id=place_id)
    gas_station.set_prices(prices)
    return gas_station