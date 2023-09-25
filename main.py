import uvicorn
from fastapi import FastAPI

from src import api, db
from src.exception_handler import add_exception_handler
from src.config import get_app_config

config = get_app_config()

db.connect(
    db=config.db_name,
    host=config.db_host,
    username=config.db_username,
    password=config.db_password,
)

app = FastAPI()
app.include_router(api.router)
add_exception_handler(app)

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
