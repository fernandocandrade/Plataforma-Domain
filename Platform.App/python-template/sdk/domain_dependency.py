from sdk.apicore import ApiCore
import log

class DomainDependency(ApiCore):

    def __init__(self):
        super().__init__()

    def get_dependency_by_process_and_version(self, process_id, version, entities):
        params = {
            "filter":"byProcessIdAndVersionInEntities",
            "processId": process_id,
            "version": version,
            "entities": self.parse_array(entities)
        }
        return self.get("dependencyDomain", params)
