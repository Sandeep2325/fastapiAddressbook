from fastapi import FastAPI, Depends, Request
# from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base, engine,addresstablee,SessionLocal
from sqlalchemy.orm import Session
Base.metadata.create_all(engine)
app = FastAPI()
# "________________________Without Sql database______________________________________"
# adressdata={
#     1:{"city":"Bangalore","state":"Karnataka"},
#     2:{"city":"Chennai","state":"Tamil Nadu"},
#     3:{"city":"Hyderabad","state":"Telangana"},
# }
# "________________________________________________________________"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def getaddresses(db: Session = Depends(get_db)):  #to get the all the address saved in addresstablee
    records = db.query(addresstablee).all() #fetching all data
    return records  #returning the fetched objects
 
@app.get("/{id}")
def getaddress(id:int,db: Session = Depends(get_db)):#to retrieve the individual data using objects Id
    record = db.query(addresstablee).filter(addresstablee.id==id).first()#filtering the objects for given Id
    return record

@app.post("/")
def add_address(id:int,city:str,state:str,landmark:str,db: Session = Depends(get_db)): #Creating New address objects 
    
    if city!= "" and state!="" and landmark!="": #validating the values if its null or not, if values are not null then creating the object
        session = Session(bind=engine, expire_on_commit=False)#binding the database table to the sessin
        add = addresstablee(city = city,state=state,landmark=landmark)#new object will be created with auto generated unique ID
        session.add(add) #add the object to the Session on which our table is binded
        session.commit()
        session.close()
        records = db.query(addresstablee).all()#getting all the data after creating the new instance
        return records
    else:
        return {"message":"Update every fields"} #returning Validated message if Atleast one field is none

@app.put("/")
def update_address(id:int,city:str,state:str,landmark:str,db: Session = Depends(get_db)):#updated the object using the given Id
  
    if city!= "" and state!="" and landmark!="":
        try:
            addre = db.query(addresstablee).get(id) #getting the object for passed id to update
            addre.city=city  #updating city
            addre.state=state #updating State
            addre.landmark=landmark #updating landmark
            db.commit()# commiting the changes
            db.refresh(addre)#refreshing instance after changes
            # adressdata[id] = {"city":city,"state":state}
            return addre
        except:
            return {"message":"No matching Id to update"} #returning message if Passed id doesn't exists
    else:
        return {"message":"Please Update every field"}#returning message every field is not updated

@app.delete("/")
def delete_address(id:int,db: Session = Depends(get_db)):#To delete the object using passed Id
   
    try:
        addre = db.query(addresstablee).get(id)#getting the instance of passed id
        db.delete(addre) #deleting the instance/object from table 
        db.commit()#commiting changes
        return {"message":f"{id} object Deleted successfully"} #returing the Successfull message after deleting the instance
    except:
        return {"message":"No Records to delete"} #returing the message if matching id instance is not exists

# @app.get("/location/{location}")
def searchAddress(search:str,db: Session = Depends(get_db)):#function to get the searched input
    # print(city)
    try:
        record = db.query(addresstablee).filter(addresstablee.landmark.contains(search)).first() or db.query(addresstablee).filter(addresstablee.city.contains(search)).first() or db.query(addresstablee).filter(addresstablee.state.contains(search)).first()#searching for the object for given input in all the columns
       
        return record #returning the filtered objects 
    except:
       return {"message":"No Data for your search"}#returning message if no data exists for given search

@app.get("/location/{location}")
def search(db: Session = Depends(get_db), search:str = None):#search API to search objects in DB by given input
    jobs = searchAddress(search, db=db)#passing the searched parameter to the searchAddress function
    return jobs 