import aioredis
from .resolver import Resolver
import json

class Connection:

    def __init__(self,
                 loop,
                 host='localhost',
                 port=6379,
                 username=None,
                 password=None,
                 database=1,
                 minsize=10,
                 maxsize=15):
        self.loop = loop
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.minsize = minsize
        self.maxsize = maxsize
        self._con = None
        self.Resolver = Resolver(self)

    @property
    def full_url(self) -> str:
        return f'redis://{self.host}'

    async def init_connection(self) -> None:
        self._con = await aioredis.create_redis_pool(address=self.full_url,
                                                     minsize=self.minsize,
                                                     maxsize=self.maxsize,
                                                     loop=self.loop)

