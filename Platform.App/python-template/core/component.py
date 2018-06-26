from settings.loader import Loader


class Component:
    def __init__(self):
        self.config = Loader().load()

    def is_apicore(self):
        return self.config["app"]["name"] == "apicore"

    def system_id(self):
        return self.config["solution"]["id"]
