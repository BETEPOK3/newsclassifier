from sqlalchemy import MetaData,  Integer, String, Column,  Boolean
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'
    metadata = metadata
    id = Column(Integer(), primary_key=True, autoincrement=True)
    data = Column(String(), unique=True, nullable=False)
