import json
from fastapi import FastAPI, Depends, HTTPException, status
from mangum import Mangum
from .aws import s3_res, BUCKET
from .gas_station import GasStation, Prices
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import auth

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

wsgi = Mangum(app)


@app.get('/pbras/prices')
async def get_pbras_prices() -> dict:
    pbras_prices = s3_res.Object(BUCKET, 'prices/pbras.prices.json')
    return json.load(pbras_prices.get().get('Body'))


@app.get('/gas_station/{place_id}/price')
def get_gas_station_price(place_id: str):
    gas_station = GasStation(place_id=place_id)
    try:
        gas_station.get_prices()
    except:
        return gas_station


@app.post('/gas_station/{place_id}/price')
def set_gas_station_price(place_id: str, item: Prices):

    prices = Prices.parse_obj(item)
    gas_station = GasStation(place_id=place_id)
    gas_station.set_prices(prices)
    return gas_station


@app.get("/users/me")
async def read_users_me(current_user: auth.User = Depends(auth.get_current_active_user)):
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(auth.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await auth.Token.from_user(user)
