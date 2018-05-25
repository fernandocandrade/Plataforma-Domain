
from sdk.apicore import ApiCore


class Branch(ApiCore):

    def __init__(self):
        super().__init__()

    def set_merged(self, branch):
        data = {}
        data["systemId"] = self.system_id()
        data["name"] = branch
        data["status"] = "merged"
        data["_metadata"] = {
            "type":"branch",
            "changeTrack":"update"
        }
        self.persist([data])