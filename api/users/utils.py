import random
from faker import Faker
from django.conf import settings
from .models import User


faker = Faker()


def generate_username(
    prefix=None,
    separators=["", "-", "_"],
    max_attempts=settings.USERNAME_GENERATION_MAX_ATTEMPTS,
):
    prefix = prefix if prefix else faker.word()
    for _ in range(max_attempts):
        separator = random.choice(separators)
        postfix = random.choice([faker.word(), random.randint(1, 99999)])
        username = f"{prefix}{separator}{postfix}"[
            : settings.USERNAME_MAX_LENGTH
        ]
        if not User.objects.filter(username=username).exists():
            return username
