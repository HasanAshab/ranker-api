import json
from ranker.common.gpt import GroqGPTCompletion


class ChallengeStepsGPTCompletion(GroqGPTCompletion):
    PROMPT = """Break a challenge into several (maximum 5) steps.
    You will be given the challenge.
    Your response should be in the format of array of strings (JSON).
    I will parse your response as json so no extra spaces and talks.
    example: ["Foo", "Bar", "Baz"]
    """

    FALLBACK_RESULT = [
        "Identify the main objective",
        "Break down the objective into smaller steps",
        "Assign deadlines to each steps",
        "Gather necessary resources",
        "Review and adjust the plan",
    ]

    def clean_result(self, result):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result

    def is_valid_result(self, result):
        return isinstance(result, list) and all(
            isinstance(step, str) for step in result
        )
