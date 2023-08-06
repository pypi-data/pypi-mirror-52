from .mapper import Mapper

from redisobjects.serializer import StringSerializer
from redisobjects import RedisIndexAtom

class IndexMapper(Mapper):
    def __init__(self, value_serializer=StringSerializer()):
        self.value_serializer = value_serializer

    def map(self, space, name, db, key, partial_key):
        return RedisIndexAtom(db, partial_key, space.keyspace, name, space.key_serializer, self.value_serializer)
