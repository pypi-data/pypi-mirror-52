from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String


engine = create_engine('sqlite:///parser.db', echo=True)
Base = declarative_base()


class Domain(Base):
    __tablename__ = 'domain'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Domain ('%s')>" % self.name


Base.metadata.create_all(engine)

