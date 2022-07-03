from typing import Any, List, Optional
import geopy.distance
import googlemaps
from pydantic import BaseModel
from ..settings import settings

client = googlemaps.Client(key=settings.GOOGLEMAPS_API_KEY)

class Location(BaseModel):
    lat: float
    lng: float

    @property
    def set(self):
        return (self.lat, self.lng)

class PlacesResultGeometry(BaseModel):
    location: Location
    #       viewport': {
    #           northeast': {
    #               lat': -23.59114462010728,
    #               lng': -46.64667487010728},
    #           southwest': {
    #               lat': -23.59384427989272,
    #               lng': -46.64937452989273
    #         }
    #     }
    # },


class PlacesResult(BaseModel):
    business_status: str #'OPERATIONAL',
    geometry: PlacesResultGeometry
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

class AddressComponent(BaseModel):
    long_name: str  # 'São Paulo'
    short_name: str  # 'São Paulo'
    types: List[str]  # [ 'administrative_area_level_2', political']

class Bounds(BaseModel):
    # { 'northeast': {'lat': -23.597, 'lng': -46.6525},
    #                           southwest': { 'lat': -23.597125,
    #                                          lng': -46.652625}},
    #               location': {'lat': -23.597046, 'lng': -46.6526055},
    #               location_type': 'GEOMETRIC_CENTER',
    #               viewport': { 'northeast': { 'lat': -23.5957135197085,
    #                                            lng': -46.65121351970851},
    #                             southwest': { 'lat': -23.5984114802915,
    #                                            lng': -46.65391148029151}}
    location: Location
    location_type: Any


class ReverseLocation(BaseModel):
    address_components: List[AddressComponent]
    formatted_address: str #'C83W+5X São Paulo, State of São Paulo, Brazil',
    geometry: Bounds
    place_id: str # 'GhIJJjW0AdiYN8ARSdi3k4hTR8A',
    plus_code: Optional[dict]
    # { 'compound_code': 'C83W+5X São Paulo, State of São Paulo, '
                #                     Brazil',
                #    global_code': '588MC83W+5X'},
    types: Optional[List[str]]#['plus_code']}

    def __get_addr_by_type(self, type: str) -> AddressComponent:
        for addr in self.address_components:
            if type in addr.types:
                return addr

    @property
    def location(self):
        return self.geometry.location

    @property
    def country(self):
        return self.__get_addr_by_type('country')

    @property
    def street_number(self):
        return self.__get_addr_by_type('street_number')

    @property
    def state(self):
        return self.__get_addr_by_type('administrative_area_level_1')

    @classmethod
    def reverse_geocode(cls, lat: float, lng: float):
        for res in client.reverse_geocode((lat,lng)):
            res = cls.parse_obj(res)
            # Only return _exact_ match
            if res.geometry.location.lat == lat and \
                res.geometry.location.lng == lng:
                return res



# long_name='1601' short_name='1601' types=['street_number']
# long_name='Rua Pedro de Toledo' short_name='Rua Pedro de Toledo' types=['route']
# long_name='Vila Clementino' short_name='Vila Clementino' types=['political', 'sublocality', 'sublocality_level_1']
# long_name='São Paulo' short_name='São Paulo' types=['administrative_area_level_2', 'political']
# long_name='São Paulo' short_name='SP' types=['administrative_area_level_1', 'political']
# long_name='04039-034' short_name='04039-034' types=['postal_code']