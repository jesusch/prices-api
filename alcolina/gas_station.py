from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from .aws import BUCKET, s3_res


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
