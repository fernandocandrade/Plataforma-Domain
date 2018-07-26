
from sdk.apicore import ApiCore
import log
"""
systemId:
      column: system_id
    processId:
      column: process_id
    name:
      column: name
    event_in:
      column: event_in
    event_out:
      column: event_out
    image:
      column: image
    commit:
      column: commit
    version:
      column: version
    reprocessable:
      column: reprocessable
"""
class OperationDTO:
    def __init__(self, **kwargs):
        self.system_id = kwargs.get('systemId')
        self.process_id = kwargs.get('processId')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.event_in = kwargs.get('event_in')
        self.event_out = kwargs.get('event_out')
        self.image = kwargs.get('image')
        self.commit = kwargs.get('commit')
        self.version = kwargs.get('version')
        self.reprocessable = kwargs.get('reprocessable')

class Operation(ApiCore):

    def __init__(self):
        super().__init__()

    def find_by_name_and_version(self, name,version):
        params = {
            "filter":"byEventAndVersion",
            "event": name,
            "version": version,
        }
        result = self.get("operation", params)
        op = list(map(lambda x : OperationDTO(**x), result))
        if len(op) == 1:
            return op[0]
        return None