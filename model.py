from typing import TypeVar, Optional
from pydantic import BaseModel

"""
model.py: Contiene las clases y atributos de las diferentes colecciones de la base de datos y el Response
"""

T = TypeVar('T')

class Booking(BaseModel):
    user_id: str
    trip_id: str
    status: str
    
class Message(BaseModel):
    sender_id: str
    recipient_id: str
    content: str
    date: str
    
class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None 
    
class Review(BaseModel):
    reviewer_id: str
    driver_id: str
    rating: int
    comment: str
    date: str
    
class Trip(BaseModel):
    driver_id: str
    start_location: str
    departure_time: str
    available_places: int
    price: int
    trip_type: str
    day: str
    end_date: str
    arrival_location: str

class User(BaseModel):
    name: str
    last_name: str
    bio: str
    password: str
    email_address: str
    municipality: str
    zip_code: str