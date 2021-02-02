import json


class Command:
    """
    Abstract Base Class for all commands.
    """
    class Error(Exception):
        pass

    def __init__(self, context):
        self._context = context

    def execute(self):
        print("MERKELY_COMMAND={}".format(self.name))
        self._required_env("MERKELY_COMMAND")
        self._required_env("MERKELY_API_TOKEN")
        self._required_env("MERKELY_HOST")
        self._verify_args()  # Template Method Pattern
        self._concrete_execute()  # Template Method Pattern

    @property
    def name(self):
        return self._required_env("MERKELY_COMMAND")

    @property
    def api_token(self):
        return self._env("MERKELY_API_TOKEN")

    @property
    def host(self):
        return self._env("MERKELY_HOST")

    @property
    def merkelypipe(self):
        try:
            merkelypipe_path = "/Merkelypipe.json"
            with open(merkelypipe_path) as file:
                return json.load(file)
        except FileNotFoundError:
            raise self.Error(f"{merkelypipe_path} file not found")
        except IsADirectoryError:
            raise self.Error(f"{merkelypipe_path} is a directory")
        except json.decoder.JSONDecodeError as exc:
            raise self.Error(f"{merkelypipe_path} invalid json - {str(exc)}")

    def _required_env(self, key):
        value = self._env(key)
        if value is None:
            raise self.Error(f"{key} environment-variable not set")
        if value == "":
            raise self.Error(f"{key} environment-variable is empty string")
        return value

    def _env(self, key):
        return self._context.env.get(key, None)
