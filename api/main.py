from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dataBase import SessionLocal, engine
import models as models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
origins = [
    "https://lkr-viagens.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Modelos Pydantic
class UserBase(BaseModel):
    user: str
    password: str

    class Config:
        orm_mode = True

class UserModel(UserBase):
    userId: int

class TripBase(BaseModel):
    departureDate: str
    returnDate: str
    destiny: str
    typeDestiny: str
    typeTrip: str
    description: str

    class Config:
        orm_mode = True

class TripModel(TripBase):
    id: int
    userId: int

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criação das tabelas
models.Base.metadata.create_all(bind=engine)

# Endpoints para usuários
@app.post("/users/", response_model=UserModel)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.User(user=user.user, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserModel])
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserModel)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userId == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}/trips/", response_model=List[TripModel])
async def read_user_trips(user_id: int, db: Session = Depends(get_db)):
    trips = db.query(models.Trip).filter(models.Trip.userId == user_id).all()
    if not trips:
        raise HTTPException(status_code=404, detail="No trips found for this user")
    return trips

@app.post("/users/{user_id}/trips/", response_model=TripModel)
async def create_trip_for_user(user_id: int, trip: TripBase, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    db_user = db.query(models.User).filter(models.User.userId == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_trip = models.Trip(
        departureDate=trip.departureDate,
        returnDate=trip.returnDate,
        destiny=trip.destiny,
        typeDestiny=trip.typeDestiny,
        typeTrip=trip.typeTrip,
        description=trip.description,
        userId=user_id
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@app.delete("/users/{trip_id}/trips/", response_model=TripModel)
async def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(db_trip)
    db.commit()
    return db_trip

@app.put("/trips/{trip_id}/", response_model=TripModel)
async def update_trip(trip_id: int, trip: TripBase, db: Session = Depends(get_db)):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    update_data = trip.dict(exclude_unset=True)  # Somente campos que foram passados
    for key, value in update_data.items():
        setattr(db_trip, key, value)
    
    db.commit()
    db.refresh(db_trip)
    return db_trip
