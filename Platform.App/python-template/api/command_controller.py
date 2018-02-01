""" Command Controller persist data on domain """
class CommandController:
    def __init__(self, app_id, request, mapper):
        self.app_id = app_id
        self.request = request
        self.mapper = mapper

    def persist(self):
        """ Persist data on domain """
        return []
