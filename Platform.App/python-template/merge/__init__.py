import log
from sdk.branch_link import BranchLink
from sdk.process_memory import head

class MergeBranch:
    def __init__(self, session):
        self.session = session
        self.branch_link = BranchLink()
        pass

    def get_event(self, instance_id):
        context = head(instance_id)
        return context.get("event")

    def run(self, instance_id):

        self.branch_link.get_links_by_branch("cenario-01")
        log.info("Running merge branch")