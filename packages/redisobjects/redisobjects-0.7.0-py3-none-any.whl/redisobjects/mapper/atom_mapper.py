from .mapper import Mapper

from redisobjects.serializer import StringSerializer
from redisobjects import RedisAtom

class AtomMapper(Mapper):
    def __init__(self, value_serializer=StringSerializer()):
        self.value_serializer = value_serializer

    def map(self, space, name, db, key, partial_key):
        return RedisAtom(db, key, self.value_serializer)
