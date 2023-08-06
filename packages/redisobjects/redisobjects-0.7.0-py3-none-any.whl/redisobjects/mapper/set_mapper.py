from .mapper import Mapper

from redisobjects.serializer import StringSerializer
from redisobjects import RedisSet

class SetMapper(Mapper):
    def __init__(self, value_serializer=StringSerializer()):
        self.value_serializer = value_serializer

    def map(self, space, name, db, key, partial_key):
        return RedisSet(db, key, self.value_serializer)
