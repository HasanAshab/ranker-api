from django.db import transaction
from .gpt import ChallengeStepsGPTCompletion
from .models import Challenge, ChallengeStep


def generate_challenge_steps(challenge: Challenge) -> list[ChallengeStep]:
    completion = ChallengeStepsGPTCompletion(challenge.title)
    challenge_steps_titles = completion.create()
    challenge_steps = [
        ChallengeStep(title=title, challenge=challenge)
        for title in challenge_steps_titles
    ]
    with transaction.atomic():
        challenge.steps.all().delete()
        challenge_steps = ChallengeStep.objects.bulk_create(challenge_steps)
    return challenge_steps
