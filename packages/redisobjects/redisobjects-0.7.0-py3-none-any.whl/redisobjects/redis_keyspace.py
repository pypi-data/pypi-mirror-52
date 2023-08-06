from .serializers import IdentitySerializer
from .redis_object_factory import RedisObjectFactory

from shortuuid import uuid

class RedisKeyspace(RedisObjectFactory):
    def __init__(self, connection, keyspace='?', key_serializer=IdentitySerializer(), key_factory=lambda: str(uuid())):
        RedisObjectFactory.__init__(self, connection)
        self.key_serializer = key_serializer
        self.placeholder = '?'
        self.keyspace = keyspace
        self.key_factory = key_factory

    def _make_key(self, key=None):
        if key is None:
            key = self.key_factory()
        serialized_key = self.key_serializer.serialize(key)
        complete_key = self.keyspace.replace(self.placeholder, serialized_key)
        if self.placeholder in complete_key:
            raise RuntimeError('Not all placeholders have been replaced for `%s`' % (complete_key,))
        return complete_key
