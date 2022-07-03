from fastapi import FastAPI, Depends, HTTPException, status
from mangum import Mangum
from .gas_station import router as gas_station
from .auth import router as auth

app = FastAPI()
app.include_router(auth)
app.include_router(gas_station)


wsgi = Mangum(app)
