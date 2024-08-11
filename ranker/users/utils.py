import math
from django.conf import settings
from django.db import transaction
from ranker.common.utils import chunk_queryset


def calculate_level(xp: int) -> int:
    return 1 + math.floor(xp / settings.XP_PER_LEVEL)


def update_ranking(chunk: int) -> None:
    from ranker.users.models import User

    users = User.objects.all().order_by("-total_xp", "-date_joined")
    current_rank = 1
    for chunk in chunk_queryset(users, chunk):
        for user in chunk:
            user.rank = current_rank
            current_rank += 1

        with transaction.atomic():
            User.objects.bulk_update(chunk, ["rank"])
