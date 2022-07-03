from datetime import datetime
from functools import partial
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from ..aws import s3_res
from ..settings import settings
from .gmaps import PlacesResult

geolocator = Nominatim(user_agent="alcolina")
reverse = partial(geolocator.reverse, language="en")

class Prices(BaseModel):
    dt: datetime = datetime.utcnow()
    """UTC"""
    etanol: float = 0
    gasolina: float = 0


class GasStation(PlacesResult):
    prices: Prices = Prices()

    @property
    def s3_obj(self):
        return s3_res.Object(settings.BUCKET, f'prices/stations/station={self.place_id}/prices.json')

    def get_prices(self):
        data = self.s3_obj.get().get('Body').read()
        self.prices = Prices.parse_raw(data)
        return self.prices

    def set_prices(self, prices: Prices):
        self.prices = prices
        self.s3_obj.put(Body=prices.json())
