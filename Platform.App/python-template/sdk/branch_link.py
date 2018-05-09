from sdk.apicore import ApiCore


class BranchLink(ApiCore):

    def __init__(self):
        super().__init__()

    def get_links(self):
        return self.get_by_system_id("branchLink")

    def get_links_by_branch(self, branch):
        params = {
            "filter":"bySystemIdAndBranchName",
            "systemId": self.system_id(),
            "branch": branch
        }
        return self.get("branchLink", params)

    def save(self, items):
        for i in items:
            i["systemId"] = self.system_id()
            i["_metadata"] = {
                "type":"branchLink",
                "changeTrack":"create"
            }
        self.persist(items)