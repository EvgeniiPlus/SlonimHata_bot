from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Flat(Base):
    __tablename__ = 'flat'

    id = Column(Integer, primary_key=True)
    flat_id = Column(String)
    link = Column(String)
    price = Column(String)
    address = Column(String)
    description = Column(String)
    img_link = Column(String, nullable=True)


class Database:
    def __init__(self, db_url='sqlite:///flats.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def create(self, model, data):
        session = self.get_session()
        try:
            db_object = model(**data)
            session.add(db_object)
            session.commit()
            return db_object
        except Exception as e:
            session.rollback()
            print(f'Failed to create: {e}')
            return None
        finally:
            session.close()

    def get(self, model, object_id):
        session = self.get_session()
        try:
            return session.query(model).filter(model.flat_id == object_id).first()
        finally:
            session.close()

    def get_all(self, model):
        session = self.get_session()
        try:
            return session.query(model).all()
        finally:
            session.close()
