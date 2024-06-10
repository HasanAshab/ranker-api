import random
from typing import Optional
from faker import Faker
from django.conf import settings


faker = Faker()


def generate_name_from_username(username: str) -> str:
    return (
        username.replace("@", " ")
        .replace(".", " ")
        .replace("+", " ")
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )


def generate_username(
    prefix: Optional[str] = None,
    separators: Optional[list[str]] = ["", "-", "_"],
    max_attempts: Optional[int] = settings.USERNAME_GENERATION_MAX_ATTEMPTS,
) -> Optional[str]:
    from ranker.users.models import User

    prefix = prefix if prefix else faker.word()
    for _ in range(max_attempts):
        separator = random.choice(separators)
        postfix = random.choice([faker.word(), random.randint(1, 99999)])
        username = f"{prefix}{separator}{postfix}"[
            : settings.USERNAME_MAX_LENGTH
        ]
        if not User.objects.filter(username=username).exists():
            return username
