from abc import abstractmethod
from groq import Groq
from django.conf import settings


class BaseGPTCompletion:
    MAX_ATTEMPTS = 3
    FALLBACK_RESULT = None
    API_KEY = None

    @property
    @abstractmethod
    def PROMPT():
        pass

    client = None

    def __init__(self, message):
        self._message = message
        self._client = self.get_client()

    def get_client(self):
        return self.client(api_key=self.get_api_key())

    def get_api_key(self):
        if not self.API_KEY:
            raise Exception("API key is not set")
        return self.API_KEY

    def get_fallback_result(self):
        return self.FALLBACK_RESULT

    def get_result(self):
        completion = self._client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.PROMPT},
                {"role": "user", "content": self._message},
            ],
        )
        return completion.choices[0].message.content

    def clean_result(self, result):
        return result

    def is_valid_result(self, result):
        return True

    def create(self, max_attempts=None):
        max_attempts = max_attempts or self.MAX_ATTEMPTS
        for _ in range(max_attempts):
            if result := self.generate():
                return result
        return self.get_fallback_result()

    def generate(self):
        dirty_result = self.get_result()
        result = self.clean_result(dirty_result)
        if self.is_valid_result(result):
            return result


class GroqGPTCompletion(BaseGPTCompletion):
    MODEL = "llama3-8b-8192"
    client = Groq

    def get_api_key(self):
        return settings.GROQ_API_KEY
