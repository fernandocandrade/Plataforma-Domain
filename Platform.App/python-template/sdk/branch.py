
from sdk.apicore import ApiCore

"""
systemId:
      column: system_id
    name:
      column: name
    description:
      column: description
    owner:
      column: owner
    startedAt:
      column: started_at
    status:
      column: status
"""
class BranchDTO:
    def __init__(self, **kwargs):
        self.system_id = kwargs.get('systemId')
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')

class Branch(ApiCore):

    def __init__(self):
        super().__init__()

    def find_by_name(self, name):
        params = {
            "filter":"bySystemIdAndName",
            "systemId": self.system_id(),
            "name": name
        }
        result = self.get("branch", params)
        return list(map(lambda x : BranchDTO(**x), result))

    def set_merged(self, branch):
        branches = self.find_by_name(branch)
        if not branches:
            raise Exception(f"branch {branch} in system id {self.system_id()}")
        to_up = []
        for b in branches:
            data = {}
            data["id"] = b.id
            data["status"] = "merged"
            data["_metadata"] = {
                "type":"branch",
                "changeTrack":"update"
            }
            to_up.append(data)
        self.persist(to_up)

    def set_dropped(self, branch, user):
        branches = self.find_by_name(branch)
        if not branches:
            raise Exception(f"branch {branch} in system id {self.system_id()}")
        to_up = []
        for b in branches:
            data = {}
            data["id"] = b.id
            data["owner"] = user
            data["status"] = "dropped"
            data["_metadata"] = {
                "type":"branch",
                "changeTrack":"update"
            }
            to_up.append(data)
        self.persist(to_up)