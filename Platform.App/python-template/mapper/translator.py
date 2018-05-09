from core.component import Component
import log

class Translator(Component):
    def __init__(self, index):
        Component.__init__(self)
        self.index = index

    def to_domain(self, app_id, mapped):
        """ converts mapped data to domain data """
        if not "_metadata" in mapped:
            return mapped.copy()

        map_type = mapped['_metadata']['type']
        _map = self.index.get_map(app_id, map_type)
        translated = dict()
        translated['_metadata'] = mapped['_metadata']

        if "model" not in _map:
            raise AttributeError(f"App Id {app_id} or Map Type {map_type} is invalid")

        translated['_metadata']['type'] = _map['model']
        _list = self.index.columns_from_map_type(app_id, map_type)

        for _from, _to in _list:
            if _from in mapped:
                translated[_to] = mapped[_from]
        return translated

    def to_map(self, app_id, mapped):
        """ convert domain object to mapped object """
        if not "_metadata" in mapped:
            return mapped.copy()

        map_type = self.index.get_map_type_by_domain_type(
            app_id, mapped['_metadata']['type'])
        _map = self.index.get_map(app_id, map_type)
        translated = dict()
        translated['_metadata'] = {'type': map_type, 'branch': mapped.get('branch', 'master')}
        _list = self.index.columns_from_map_type(app_id, map_type)
        mapped.pop('branch', None)
        for _to, _from in _list:
            if _from in mapped:
                translated[_to] = mapped[_from]
        return translated
