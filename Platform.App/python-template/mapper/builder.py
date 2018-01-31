from mapper.index import Index
from mapper.loader import Loader
from mapper.transform import Transform
from mapper.translator import Translator

class MapBuilder:
    def build(self):
        maps = Loader().build()
        index = Index()
        index.parse(maps)
        transform = Transform(index)
        translator = Translator(index)
        return Mapper(index,transform,translator)

class Mapper:
    def __init__(self, index, transform, translator):
        self.index = index
        self.transform = transform
        self.translator = translator

