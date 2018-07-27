from model.domain import *
import log
from core.component import Component
from sdk.branch_link import BranchLink
from datetime import datetime
from uuid import uuid4
import json

class Persistence(Component):

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.branch_link = BranchLink()

    def commit(self):
        self.session.commit()

    def link_branch(self, items):
        if self.is_apicore():
            return
        current_links = self.branch_link.get_links()
        new_links = self.get_branches_to_link(items)
        new_links_to_persist = self.diff_branch_links(new_links, current_links)
        self.branch_link.save(new_links_to_persist)

    def diff_branch_links(self, incomming_links, current_links):
        result = []
        keys = [self.get_key_from_metadata(item) for item in current_links]
        for l in incomming_links:
            key = self.get_key_from_metadata(l)
            if key in keys:
                continue

            branch = l.get("branch","master")
            result.append({"entity": l["type"], "branchName":branch})
        return result

    def get_key_from_metadata(self,item):
        return item.get("type", item.get("entity", ""))+":"+item.get("branch",item.get("branchName","master"))

    def get_branches_to_link(self, items):
        result = []
        linked = set()
        for item in items:
            if "_metadata" not in item:
                continue
            key = self.get_key_from_metadata(item["_metadata"])
            if key in linked:
                continue
            linked.add(key)
            result.append(item["_metadata"])
        return result

    def persist(self, objs,scope):
        """ split object collection into 3 operation list for
            creating, updating, destroying looking for changeTrack
            on each object
        """
        self.link_branch(objs)
        to_create = []
        to_update = []
        to_destroy = []
        to_recover = []
        for o in objs:
            if not self.is_valid_changed_obj(o):
                continue
            if self.is_to_create(o):
                to_create.append(o)
            elif self.is_to_update(o):
                to_update.append(o)
            elif self.is_to_destroy(o):
                to_destroy.append(o)
            elif self.is_to_recover(o):
                to_recover.append(o)
        result = list(self.create(to_create))
        result += list(self.update(to_update,scope))
        result += list(self.recover(to_recover,scope))
        self.destroy(to_destroy,scope)
        return result

    def create(self, objs):
        for o in objs:
            _type = o["_metadata"]["type"].lower()
            rid = o["_metadata"].get("rid",None)
            if not rid:
                log.info("rid not pass will be created a new one")
                rid = uuid4()
            instance = globals()[_type](**o)
            instance.modified = datetime.utcnow()
            instance.created_at = datetime.utcnow()
            instance.rid = rid
            self.session.add(instance)
            yield instance

    def update(self, objs,scope):
        for o in objs:
            branch = o["_metadata"].get("branch","master")
            _type = o["_metadata"]["type"].lower()
            freeze = o["_metadata"].get("freeze",False)
            cls = globals()[_type]
            instance = cls(**o)
            if not instance.deleted:
                instance.deleted = False
            del o['_metadata']
            obj = self.session.query(cls).filter(cls.id == o["id"]).filter(cls.branch == branch).one_or_none()
            if not obj and branch != "master":
                #make a copy from master object to branch object
                obj = self.session.query(cls).filter(cls.id == o["id"]).filter(cls.branch == "master").one()
                setattr(instance,"from_id", obj.rid)
                setattr(instance,"rid", uuid4())
                setattr(instance,"branch", branch)
                #setattr(instance,"modified", obj.modified)
                setattr(instance,"modified", obj.modified)
                setattr(instance,"created_at", obj.created_at)
                attrs = list(obj.__dict__.items()) + list(o.items())
                for k, v in (attrs):
                    if hasattr(instance, k) and k not in {"_sa_instance_state", "rid", "from_id", "branch", "modified", "created_at"}:
                        setattr(instance, k, v)
                log.info("recreating object")
                self.session.add(instance)
            else:
                instance.modified = obj.modified
                if scope == "execution" and not freeze:
                    obj.modified = datetime.utcnow()
                for k, v in o.items():
                    if hasattr(obj, k) and k not in {"rid", "from_id", "branch", "modified", "created_at"}:
                        setattr(obj, k, v)
            yield instance

    def destroy(self, objs,scope):
        for o in objs:
            _type = o["_metadata"]["type"].lower()
            branch = o["_metadata"].get("branch","master")
            cls = globals()[_type]
            instance = cls(**o)
            if not instance.modified and scope == "execution":
                instance.modified = datetime.utcnow()
            del o['_metadata']
            obj = self.session.query(cls).filter(cls.id == o["id"]).filter(cls.branch == branch).one_or_none()
            obj.deleted = True

    def recover(self, objs,scope):
        for o in objs:
            _type = o["_metadata"]["type"].lower()
            branch = o["_metadata"].get("branch","master")
            cls = globals()[_type]
            instance = cls(**o)
            if not instance.modified and scope == "execution":
                instance.modified = datetime.utcnow()
            del o['_metadata']
            obj = self.session.query(cls).filter(cls.id == o["id"]).filter(cls.branch == branch).one_or_none()
            obj.deleted = False
            yield obj

    def is_to_create(self, obj):
        return obj["_metadata"]["changeTrack"] == "create"

    def is_to_update(self, obj):
        return obj["_metadata"]["changeTrack"] == "update" and "id" in obj

    def is_to_destroy(self, obj):
        return obj["_metadata"]["changeTrack"] == "destroy" and "id" in obj

    def is_to_recover(self, obj):
        return obj["_metadata"]["changeTrack"] == "recover" and "id" in obj

    def is_valid_changed_obj(self, obj):
        if not "_metadata" in obj:
            return False
        if not "changeTrack" in obj["_metadata"]:
            return False
        if obj["_metadata"]["changeTrack"] not in ["create", "update", "destroy"]:
            return False
        return True
