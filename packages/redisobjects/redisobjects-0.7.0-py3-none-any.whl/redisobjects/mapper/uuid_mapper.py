from .atom_mapper import AtomMapper
from redisobjects.serializer import UUIDSerializer

class UUIDMapper(AtomMapper):
    def __init__(self):
        AtomMapper.__init__(self, UUIDSerializer())
