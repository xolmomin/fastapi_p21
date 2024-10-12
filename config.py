import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv
from fastapi_storages import FileSystemStorage
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


conf = Configuration()

storage = FileSystemStorage(path="media/")
templates = Jinja2Templates(directory='templates')
