import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends

from .aws import BUCKET, s3_res
from . import auth

router = APIRouter(prefix='/gas_station', tags=['gas_station'])


class Prices(BaseModel):
    dt: datetime = datetime.utcnow()
    """UTC"""
    etanol: float = 0
    gasolina: float = 0


class GasStation(BaseModel):
    place_id: str #'ChIJ10tPiiBazpQRaMAucpT99xE',
    prices: Prices = Prices()

    @property
    def s3_obj(self):
        return s3_res.Object(BUCKET, f'prices/stations/station={self.place_id}/prices.json')

    def get_prices(self):
        data = self.s3_obj.get().get('Body').read()
        self.prices = Prices.parse_raw(data)
        return self.prices

    def set_prices(self, prices: Prices):
        self.prices = prices
        self.s3_obj.put(Body=prices.json())


@router.get('/pbras/prices')
async def get_pbras_prices(current_user: auth.User = Depends(auth.get_current_active_user)) -> dict:
    pbras_prices = s3_res.Object(BUCKET, 'prices/pbras.prices.json')
    return json.load(pbras_prices.get().get('Body'))

@router.get('/{place_id}/price')
def get_gas_station_price(place_id: str, current_user: auth.User = Depends(auth.get_current_active_user)):
    gas_station = GasStation(place_id=place_id)
    try:
        gas_station.get_prices()
    except:
        return gas_station


@router.post('/{place_id}/price')
def set_gas_station_price(place_id: str, item: Prices, current_user: auth.User = Depends(auth.get_current_active_user)):

    prices = Prices.parse_obj(item)
    gas_station = GasStation(place_id=place_id)
    gas_station.set_prices(prices)
    return gas_station