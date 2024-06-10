import math
from django.conf import settings


def calculate_level(xp: int) -> int:
    return 1 + math.floor(xp / settings.XP_PER_LEVEL)
