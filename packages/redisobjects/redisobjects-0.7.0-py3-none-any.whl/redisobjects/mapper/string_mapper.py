from .atom_mapper import AtomMapper

from redisobjects.serializer import StringSerializer

class StringMapper(AtomMapper):
    def __init__(self):
        AtomMapper.__init__(self, StringSerializer())
