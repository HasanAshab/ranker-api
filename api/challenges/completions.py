import json
from api.common.completions import GroqGPTCompletion


class ChallengeStepsGPTCompletion(GroqGPTCompletion):
    PROMPT = """Break a challenge into several (maximum 5) steps.
    You will be given the challenge.
    Your response should be in the format of array of strings (JSON).
    example: ["Foo", "Bar", "Baz"]
    I will parse your response as json so no extra spaces and talks
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
