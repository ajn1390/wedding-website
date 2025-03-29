"""
Imports all the models so that Base has them.
"""

from src.backend.app.db.base_class import Base, metadata
from src.backend.app.db.models import *

b, m = Base, metadata
