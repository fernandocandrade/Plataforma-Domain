from settings.loader import Loader


class Component:
    def __init__(self):
        self.config = Loader().load()
