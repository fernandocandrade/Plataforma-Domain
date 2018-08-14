import log
from sdk.branch_link import BranchLink
from sdk.branch import Branch
from sdk.process_memory import head
from sqlalchemy import text
from model.domain import *
from sdk import event_manager

class MergeBranch:
    def __init__(self, session):
        self.session = session
        self.branch_link = BranchLink()
        self.branch = Branch()

    def get_event(self, instance_id):
        context = head(instance_id)
        return context.get("event")

    def run(self, instance_id):
        log.info("Running merge branch")
        event = self.get_event(instance_id)
        try:
            branch_name = event.get("payload",{}).get("branch")
            log.info(f"Merging {branch_name} into master")
            if not branch_name:
                raise Exception(f"branch name should be passed! received:{branch_name}")
            log.info("Gettings branch links")
            links = self.branch_link.get_links_by_branch(branch_name)
            for link in links:
                _type = link.entity.lower()
                cls = globals()[_type]
                log.info(f"Flipping {_type}")
                self.flip_data(cls, self.session, link.branch_name)
            log.info("Closing branch on apicore")
            self.branch.set_merged(branch_name)
            log.info("Commiting changes to database")
            self.session.commit()
            log.info("Merge success")
            event["name"] = event["name"].replace(".request",".done")
            event_manager.push(event)
        except Exception as ex:
            log.critical(ex)
            if event:
                event["name"] = event["name"].replace(".request",".error")
                event["payload"]["message"] = str(ex)
                event_manager.push(event)
            else:
                event = {}
                event["name"] = "domain.merge.error"
                event["instanceId"] = instance_id
                event["payload"] = {}
                event["payload"]["instanceId"] = instance_id
                event["payload"]["message"] = str(ex)
                event_manager.push(event)
            raise ex




    def flip_data(self, cls, session, branch):
        registers = session.query(cls).filter(text(f"branch = '{branch}'")).all()
        for register in registers:
            if not register.from_id:
                new_instance = cls()
                self.assign(register, new_instance)
                new_instance.branch = "master"
                session.add(new_instance)
            else:
                origin_object = session.query(cls).filter(cls.rid == register.from_id).filter(cls.branch == "master").one()
                self.assign(register, origin_object)
                self.session.add(origin_object)

            register.branch = f"merged:{register.branch}"
            session.add(register)

    def assign(self, _from, _to):
        for k, v in _from.__dict__.items():
            if hasattr(_to, k) and k not in {"_sa_instance_state", "branch", "rid", "from_id"}:
                setattr(_to, k, v)
