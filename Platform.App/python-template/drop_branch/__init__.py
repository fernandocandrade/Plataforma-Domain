import log
from sdk.branch_link import BranchLink
from sdk.branch import Branch
from sqlalchemy import text
from model.domain import *

class DropBranch:
    def __init__(self, session):
        self.session = session
        self.branch_link = BranchLink()
        self.branch = Branch()

    def drop(self, branch_name, user):
        log.info(f"Dropping {branch_name}")
        if not branch_name:
            raise Exception(f"branch name should be passed! received:{branch_name}")
        log.info("Gettings branch links")
        links = self.branch_link.get_links_by_branch(branch_name)
        for link in links:
            _type = link.entity.lower()
            cls = globals()[_type]
            log.info(f"Dropping {_type}")
            self.drop_branch_entity(cls, self.session, link.branch_name)
        log.info("Dropping branch on apicore")
        self.branch.set_dropped(branch_name, user)
        log.info("Commiting changes to database")
        self.session.commit()
        log.info("Branch dropped with success")


    def drop_branch_entity(self, cls, session, branch):
        registers = session.query(cls).filter(text(f"branch = '{branch}'")).all()
        for register in registers:
            register.branch = f"dropped:{branch}"
            session.add(register)