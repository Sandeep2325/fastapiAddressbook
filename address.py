from fastapi import FastAPI, Depends, Request
# from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base, engine,addresstable,SessionLocal
from sqlalchemy.orm import Session
# engine = create_engine("sqlite:///address.db")
# Base = declarative_base()
# class address(Base):
#     __tablename__ = 'address_table'
#     id = Column(Integer, primary_key=True)
#     city = Column(String(256))
#     state=Column(String(256))
Base.metadata.create_all(engine)

app = FastAPI()


# "________________________Without Sql database______________________________________"
adressdata={
    1:{"city":"Bangalore","state":"Karnataka"},
    2:{"city":"Chennai","state":"Tamil Nadu"},
    3:{"city":"Hyderabad","state":"Telangana"},
}
# "________________________________________________________________"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def getaddresses(db: Session = Depends(get_db)):
    records = db.query(addresstable).all()
    return records

@app.get("/{id}")
def getaddress(id:int,db: Session = Depends(get_db)):
    record = db.query(addresstable).filter(addresstable.id==id).first()
    return record

@app.post("/")
def add_address(id:int,city:str,state:str,landmark:str,db: Session = Depends(get_db)):
    if city== "" and state=="" and landmark=="":
    # newId = len(adressdata.keys()) + 1
    # adressdata[newId] = {"city":city,"state":state}
        session = Session(bind=engine, expire_on_commit=False)
        add = addresstable(city = city,state=state,landmark=landmark)
        session.add(add)
        session.commit()
        id = add.id
        session.close()
        records = db.query(addresstable).all()
        return records
    else:
        return {"message":"Update every fields"}

@app.put("/")
def update_address(id:int,city:str,state:str,landmark:str,db: Session = Depends(get_db)):
    # newId = len(adressdata.keys()) + 1
    print("-------------------",city)
    if city== "" and state=="" and landmark=="": 
        addre = db.query(addresstable).get(id)
        addre.city=city
        addre.state=state
        addre.landmark=landmark
        db.commit()
        db.refresh(addre)
        adressdata[id] = {"city":city,"state":state}
        return addre
    else:
        return {"message":"Please Update every field"}

@app.delete("/")
def delete_address(id:int,db: Session = Depends(get_db)):
    # newId = len(adressdata.keys()) + 1
    # del adressdata[id]
    try:
        addre = db.query(addresstable).get(id)
        print("--------------------",addre)
        db.delete(addre)
        db.commit()
        return adressdata
    except:
        return {"message":"No Records to delete"}

@app.get("/location/{location}")
def searchAddress(city:str,db: Session = Depends(get_db)):
    # print(city)
    try:
        record = db.query(addresstable).filter(addresstable.city==city).first()
        print("---------------",record)
        # a=[]
        # for i in adressdata:
        #     add=adressdata[i]
        #     if city in add.values():
        #         a.append(adressdata[i])
        #     else:
        #         print("Not present")
        return record
    except:
       return {"message":"No Data for your search"}
    