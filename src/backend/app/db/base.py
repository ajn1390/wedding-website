"""
Imports all the models so that Base has them.
"""
from app.db.base_class import metadata
from app.db.base_class import Base
from app.db.models import *