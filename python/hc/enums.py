from enum import Enum


class Colors(Enum):
    RED = (1.0, 0.0, 0.0)
    GREEN = (0.0, 0.985, 0.0)
    YELLOW = (1.0, 0.85, 0.0)
    MAGENTA = (1.0, 0, 0.95)
    WHITE = (1.0, 1.0, 1.0)
    BLACK = (0.0, 0.0, 0.0)


class Actions(Enum):
    GET = 'GET'
    SET = 'SET'
    MODIFY = 'MODIFY'


class ActivityAttrs(Enum):
    TINT = '_normalized_tint'
    MOTION = '_normalized_motion'
