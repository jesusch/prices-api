import googlemaps
import geopy.distance
from pydantic import BaseModel
from .gas_station import GasStation, Prices

DISTANCE = 0.1

gmaps = googlemaps.Client(key=api_key)

class Location(BaseModel):
    lat: float
    lng: float

    @property
    def set(self):
        return (self.lat, self.lng)

class PlacesResultGeometry(BaseModel):
    location: Location


class PlacesResult(BaseModel):
    business_status: str #'OPERATIONAL',
    geometry: PlacesResultGeometry
    #     'location': {
    #         'lat': -23.5924086,
    #         'lng': -46.6479811
    #     },
    #     'viewport': {
    #         'northeast': {
    #             'lat': -23.59114462010728,
    #             'lng': -46.64667487010728},
    #         'southwest': {
    #             'lat': -23.59384427989272,
    #             'lng': -46.64937452989273
    #         }
    #     }
    # },
    # icon: str 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/gas_station-71.png',
    # 'icon_background_color': '#909CE1',
    # 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/gas_pinlet',
    name: str # 'Posto Shell',
    opening_hours: dict  = {
        'open_now': True
    }
    # 'photos': [
    #     {'height': 3186, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/117684703793862723952">Tânia Mara Francisco</a>'], 'photo_reference': 'Aap_uEAWii_sgCF1f-9qM8N46H0veJhFdWthlpkg2A82XuOPFPOb2L8beP9atnbei32tTTsGq7XWUqXlkUH0EurYI1_mZhMWy48rouQXIaPfrmQV34GPtUACN0RNJaH0aLT-V8uAs9OYMesVEg4tAEQGPz_dWOsS6pE8V_RG6xuDFOAhx4dD', 'width': 4073}
    # ],
    place_id: str #'ChIJ10tPiiBazpQRaMAucpT99xE',
    #'plus_code': {'compound_code': 'C952+2R São Paulo, State of São Paulo', 'global_code': '588MC952+2R'},
    # 'price_level': 2,
    # 'rating': 3.8,
    # 'reference': 'ChIJ10tPiiBazpQRaMAucpT99xE',
    # 'scope': 'GOOGLE',
    # 'types': ['gas_station', 'point_of_interest', 'establishment'],
    # 'user_ratings_total': 582,
    # 'vicinity': 'R. Sena Madureira, 1490 - Vila Clementino, São Paulo'}

    def distance(self, loc:Location):
        return geopy.distance.geodesic(self.geometry.location.set, loc.set)


def get_gas_station(loc: Location) -> GasStation:
    res = gmaps.places_nearby(
        location=loc.set,
        keyword='gas station',
        radius=DISTANCE,
        # name='gas station'
    )

    return [GasStation.parse_obj(r) for r in res.get('results')].pop(-1)

def get_gas_station_prices(gas_station: GasStation) -> GasStation:
    print(gas_station.place_id)
    return

def set_gas_station_prices(prices: Prices) -> Prices:
    print(prices.json())

    return