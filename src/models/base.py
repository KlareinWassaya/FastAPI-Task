from sqlalchemy.ext.declarative import declarative_base

from src.config.definitions import SCHEMA_NAME


class Base(declarative_base()):
    __abstract__ = True
    #__table_args__ = {"schema": SCHEMA_NAME}
    __name__: str
