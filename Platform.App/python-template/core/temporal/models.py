class TemporalModelMixin:
    temporal = tuple()

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @classmethod
    def get_module_name(cls):
        return cls.__module__

    @classmethod
    def get_clock_name(cls):
        return f"{cls.get_classname()}Clock"

    @classmethod
    def get_history_name(cls, field):
        return f"{cls.get_classname()}{field.title()}History"



