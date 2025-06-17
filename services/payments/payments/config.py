from os import getenv

class Config:
    DATABASE_URL = getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
