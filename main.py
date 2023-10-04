import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src import api, db
from src.exception_handler import add_exception_handler
from src.config import get_app_config
import os

config = get_app_config()

db.connect(
    db=config.db_name,
    host=config.db_host,
    username=config.db_username,
    password=config.db_password,
)

app = FastAPI(version="1.1")
app.include_router(api.router)
add_exception_handler(app)

os.makedirs(name="outputs/userImgs", exist_ok=True)
app.mount("/image", StaticFiles(directory="outputs/userImgs"), name="image")

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
