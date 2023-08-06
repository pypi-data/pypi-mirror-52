from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from tagcounter.DB.models.domain import Base, Domain
import pickle

engine = create_engine('sqlite:///parser.db', echo=True)


class Page(Base):
    __tablename__ = 'page'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    url = Column(String)
    date = Column(DateTime)
    tag_data = Column(LargeBinary)
    domain_id = Column(Integer, ForeignKey('domain.id'))
    domain = relationship(Domain)

    def __init__(self, url, date, tag_data, domain_id):
        self.url = url
        self.date = date
        self.tag_data = tag_data
        self.domain_id = domain_id

    def __repr__(self):
        return "<Page('%s', '%s', '%s',\n '%s')>" % (self.url, self.date, self.domain_id, pickle.loads(self.tag_data))


Base.metadata.create_all(engine)
