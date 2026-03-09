from enum import Enum, auto

class PixelStyle(Enum):
    SQUARE = auto()
    CIRCLE = auto()
    REAL = auto()

    DEFAULT = SQUARE

    @property
    def config_name(self):
        return self.name.lower()

    @classmethod
    def fetch(cls, key, default=None):
        try:
            return cls[key]
        except KeyError:
            return default or cls.DEFAULT
