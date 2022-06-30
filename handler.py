from datetime import datetime
import json
from alcolina.gas_station import GasStation, Prices
from alcolina.aws import s3_res, BUCKET


def get_id_from_event(event:dict) -> str:
    id = event.get('pathParameters', {}).get('id')
    if id is None:
        raise RuntimeError('No valid ID')
    return id


def get_pbras_prices(event, context):
    pbras_prices = s3_res.Object(BUCKET, 'prices/pbras.prices.json')
    return json.load(pbras_prices.get().get('Body'))



def get_gas_station_price(event:dict, context):
    gas_station = GasStation(place_id=get_id_from_event(event))
    prices = gas_station.get_prices()
    return prices.dict()


def set_gas_station_price(event:dict, context):
    body = json.loads(event.get('Body', '{}'))

    prices = Prices(dt=datetime.utcnow(), **body)
    gas_station = GasStation(place_id=get_id_from_event(event))
    gas_station.set_prices(prices)
    return prices.dict()



if __name__ == '__main__':
    # examples
    #pbras = Location(lat=-23.5848746, lng=-46.6443862)  # ChIJGcka-IhZzpQRDCuAT8rOlNQ
    #mobile = Location(lat=-23.6041059, lng=-46.6754449)  # ChIJu1Z4o7xQzpQREPdxo0E5RtI
    #shell = Location(lat=-23.5924086, lng=-46.6479811)  # ChIJ_bhQ0MI5zpQR7Mq50u8JyQ4
    event = {
        'pathParameters': {'id': 'ChIJGcka-IhZzpQRDCuAT8rOlNQ'},
        'Body': '{"etanol": 4.23, "gasolina": 7.23}'
    }
    print(get_gas_station_price(event, {}))