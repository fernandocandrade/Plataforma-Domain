from datetime import datetime

import pytest
from sqlalchemy import Column, String, Integer

from core.temporal.models import TemporalModelMixin


Base = pytest.BaseModel


class User(Base, TemporalModelMixin):
    name = Column(String)
    age = Column(Integer)

    class Temporal:
        fields = ('name', 'age', )

