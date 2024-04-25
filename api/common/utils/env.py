from dotenv import dotenv_values
from django.conf import settings


class EnvFile:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def open(self, mode="r"):
        return open(self.path, mode)

    def data(self):
        return dotenv_values(self.path)

    def write(self, data):
        with self.open("w") as f:
            for (
                key,
                value,
            ) in data.items():
                f.write(f"{key}={value}\n")

    def update(self, **new_data):
        data = self.data()
        data.update(new_data)
        self.write(data)
        return data


env_file = EnvFile(
    name=settings.ENV_FILE,
    path=settings.ENV_FILE_PATH,
)
