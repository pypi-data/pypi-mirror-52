from .atom_mapper import AtomMapper
from redisobjects.serializer import DateTimeSerializer

class DateTimeMapper(AtomMapper):
    def __init__(self):
        AtomMapper.__init__(self, DateTimeSerializer())
