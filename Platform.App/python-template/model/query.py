import re
from model import domain
from sqlalchemy.sql import text
import uuid
import log

class Query:
    def __init__(self, reference_date, version, session, branch='master'):
        self.reference_date = reference_date
        self.version = version
        self.session = session
        self.branch = branch
        self.app_id = None
        self.mapped_entity = None
        self.entity = None
        self.entity_cls = None

    def set_query_context(self, app_id, mapped_entity, entity):
        self.app_id = app_id
        self.mapped_entity = mapped_entity
        self.entity = entity
        self.entity_cls = getattr(domain, self.entity.lower())

    def build_select(self, projection):
        attrs = [
            getattr(self.entity_cls, a[0]).label(a[1])
            for a in projection['attributes']
        ]
        return attrs

    def execute(self, projection, page=None, page_size=None):
        query_select = self.build_select(projection)
        query = self.session.query(*query_select)
        query = query.filter(text(f"deleted = false and branch = '{self.branch}'"))

        if 'where' in projection:
            where_clause = projection["where"]["query"]
            stmt = text(where_clause).bindparams(**projection["where"]["params"])
            query = query.filter(stmt)

        if page and page_size:
            page -= 1
            query = query.slice(page * page_size, page * page_size + page_size)

        return self.row2dict(query.all(), projection)


    def history(self, mapped_entity, entity, projection, entity_id, version=None):
        domain_entity = getattr(domain, entity)
        query_select = self.build_select(projection)
        query_select.append(getattr(self.entity_cls, "deleted").label("destroy"))
        history = self.session.query(domain_entity).history(
            fields=query_select, period=self.reference_date)
        history = history.filter(domain_entity.id==entity_id)
        ranges = []
        for f in query_select:
            parts = str(f.element).split(".")
            n = parts[1]
            if n in ["id", "branch", "from_id"]:
                continue
            ranges.append(entity+n+"history.ticks")
        history = history.filter(text(f"not isEmpty({' * '.join(ranges)})"))

        ticks_fields = {
            c['name'] for c in history.column_descriptions
            if c['name'].endswith('_ticks')
        }
        for entity_history in history.all():
            entity_dict = entity_history._asdict()
            entity_dict["_metadata"] = {}
            entity_dict["_metadata"]["type"] = self.mapped_entity
            entity_dict["_metadata"]['version'] = 0
            entity_dict["_metadata"]["instance_id"] = entity_dict["meta_instance_id"]
            entity_dict["id"] = entity_id
            if entity_dict["destroy"]:
                entity_dict["_metadata"]["destroy"] = entity_dict["destroy"]
            entity_dict.pop(entity)
            entity_dict.pop("destroy")
            entity_dict.pop("meta_instance_id")
            for tick_field in ticks_fields:
                if not entity_dict[tick_field]:
                    entity_dict.pop(tick_field)
                    continue
                entity_dict["_metadata"]['version'] = max(entity_dict["_metadata"]['version'], entity_dict[tick_field])
                entity_dict.pop(tick_field)
            if (version and entity_dict["_metadata"]['version'] == int(version)) or not version:
                yield entity_dict


    def row2dict(self, rows, projection):
        d = {}
        result = []
        for row in rows:
            d = {}
            cont = 0
            instance_id = None
            for column in row:
                if type(column) == uuid.UUID:
                    column = str(column)
                if projection['attributes'][cont][1] == "meta_instance_id":
                    cont += 1
                    instance_id = column
                    continue
                d[projection['attributes'][cont][1]] = column
                cont += 1
            d["_metadata"] = {
                "type": self.mapped_entity,
                "branch":d["branch"]
            }
            d.pop("branch")
            if d["from_id"]:
                d["_metadata"]["origin"] = d["from_id"]
            d.pop("from_id")
            if instance_id:
                d["_metadata"]["instance_id"] = instance_id
            result.append(d)
        return result
