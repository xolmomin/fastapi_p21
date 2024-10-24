import os
from dataclasses import dataclass, asdict
from typing import Optional

import requests
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()


@dataclass
class BaseConfig:
    def asdict(self):
        return asdict(self)


@dataclass
class DatabaseConfig(BaseConfig):
    """Database connection variables"""
    NAME: str = os.getenv('DB_NAME')
    USER: str = os.getenv('DB_USER')
    PASS: str = os.getenv('DB_PASS')
    HOST: str = os.getenv('DB_HOST')
    PORT: str = os.getenv('DB_PORT')

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"


@dataclass
class Configuration:
    """All in one configuration's class"""
    db = DatabaseConfig()
    SECRET_KEY: str = os.getenv('SECRET_KEY')


# class CustomFileSystemStorage(FileSystemStorage):
#
#     def __init__(self, path: str) -> None:
#         self.MEDIA_URL = 'media'
#         self._path = path
#         Path(self.MEDIA_URL).mkdir(parents=True, exist_ok=True)
#
#     def get_path(self, name: str) -> str:
#         return str(self._path / Path(name))
#


def get_currency_in_sum() -> tuple[Optional[int], bool]:
    url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for currency in data:
            if currency['Ccy'] == 'USD':
                return int(float(currency['Rate'])), True
    return None, False


conf = Configuration()
# storage = CustomFileSystemStorage
templates = Jinja2Templates(directory='templates')
