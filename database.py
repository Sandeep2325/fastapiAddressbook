from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///address2.db")
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
class addresstablee(Base):
    __tablename__ = 'address_tablee'
    id = Column(Integer, primary_key=True)
    landmark=Column(String(256))
    city = Column(String(256))
    state=Column(String(256))
Base.metadata.create_all(engine)
