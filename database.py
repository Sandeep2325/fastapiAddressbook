from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///address.db")
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
class addresstable(Base):
    __tablename__ = 'address_table'
    id = Column(Integer, primary_key=True)
    city = Column(String(256))
    state=Column(String(256))
Base.metadata.create_all(engine)
