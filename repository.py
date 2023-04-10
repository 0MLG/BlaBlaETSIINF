from model import Booking, Message, Review, Trip, User
from config import database
import uuid

"""
repository.py: Contiene las consultas realizadas sobre la base de datos
"""

class BookingRepo():
    
    # getBookingsById(id:str): devuelve la reserva correspondiente al identificador
    @staticmethod
    async def getBookingById(id:str):
        return await database.get_collection('bookings').find_one({"_id":id})
    
    # getBookingsByUser(user_id:str): devuelve todas las reservas de un usuario
    @staticmethod
    async def getBookingsByUser(user_id:str):
        _bookings = []
        collection = database.get_collection('bookings').find({"user_id":user_id})
        async for booking in collection:
            _bookings.append(booking)
        return _bookings
    
    # getBookingsByTrip(trip_id:str): devuelve todas las reservas de un viaje
    @staticmethod
    async def getBookingsByTrip(trip_id:str):
        _bookings = []
        collection = database.get_collection('bookings').find({"trip_id":trip_id})
        async for booking in collection:
            _bookings.append(booking)
        return _bookings
    
    # addBooking(booking: Booking): añade una reserva a la base de datos
    @staticmethod
    async def addBooking(booking: Booking):
        id = str(uuid.uuid4())
        _booking = {
            "_id": id,
            "user_id": booking.user_id,
            "trip_id": booking.trip_id,
            "status": booking.status
        }
        await database.get_collection('bookings').insert_one(_booking)
        
    # updateBooking(id: str, booking: Booking): modifica la reserva correspondiente al id con nuevos atributos
    @staticmethod
    async def updateBooking(id:str, booking: Booking):
        _booking = await database.get_collection('bookings').find_one({"_id":id})
        _booking["user_id"] = booking.user_id
        _booking["trip_id"] = booking.trip_id
        _booking["status"] = booking.status
        await database.get_collection('bookings').update_one({"_id":id}, {"$set":_booking})
        
    # deleteBooking(id: str): elimina la reserva correspondiente al id 
    @staticmethod
    async def deleteBooking(id:str):
        await database.get_collection('bookings').delete_one({"_id":id})
        
    # bookingExists(id: str): comprueba si la reserva correspondiente al id existe en la base de datos
    @staticmethod
    async def bookingExists(id: str):
        _booking = await database.get_collection('bookings').find_one({"_id":id})
        return _booking is not None
    
class MessageRepo():
    # getMessageById(id: str): devuelve el mensaje correspondiente al identificador
    @staticmethod
    async def getMessageById(id:str):
        return await database.get_collection('messages').find_one({"_id":id})
    
    # getMessagesBySender(sender_id: str): devuelve todos los mensajes enviados por un usuario
    @staticmethod
    async def getMessagesBySender(sender_id:str):
        _messages = []
        collection = database.get_collection('messages').find({"sender_id":sender_id})
        async for message in collection:
            _messages.append(message)
        return _messages
    
    # getMessagesByRecipient(recipient_id:str): devuelve todos los mensajes recibidos por un usuario
    @staticmethod
    async def getMessagesByRecipient(recipient_id:str):
        _messages = []
        collection = database.get_collection('messages').find({"recipient_id":recipient_id})
        async for message in collection:
            _messages.append(message)
        return _messages
    
    # addMessage(message: Message): añade un mensaje a la base de datos
    @staticmethod
    async def addMessage(message: Message):
        id = str(uuid.uuid4())
        _message = {
            "_id": id,
            "sender_id": message.sender_id,
            "recipient_id": message.recipient_id,
            "content": message.content,
            "date":message.date
        }
        await database.get_collection('messages').insert_one(_message)
        
    # deleteMessage(id:str): elimina un mensaje de la base de datos
    @staticmethod
    async def deleteMessage(id:str):
        await database.get_collection('messages').delete_one({"_id":id})
        
    # messageExists(id: str): comprueba si el mensaje correspondiente al id existe en la base de datos
    @staticmethod
    async def messageExists(id: str):
        _message = await database.get_collection('messages').find_one({"_id":id})
        return _message is not None
    
class ReviewRepo():

    # getReviewsById(id:str): devuelve la reseña correspondiente al identificador
    @staticmethod
    async def getReviewById(id:str):
        return await database.get_collection('reviews').find_one({"_id":id})
    
    # getReviewsByUser(user_id:str): devuelve todas las reseñas de un usuario
    @staticmethod
    async def getReviewsByUser(user_id:str):
        _reviews = []
        collection = database.get_collection('reviews').find({"driver_id":user_id})
        async for review in collection:
            _reviews.append(review)
        return _reviews
    
    # addReview(review: Review): añade una reseña a la base de datos
    @staticmethod
    async def addReview(review: Review):
        id = str(uuid.uuid4())
        _review = {
            "_id": id,
            "reviewer_id": review.reviewer_id,
            "driver_id": review.driver_id,
            "rating": review.rating,
            "comment": review.comment,
            "date": review.date
        }
        await database.get_collection('reviews').insert_one(_review)
        
    # updateReview(id: str, review: Review): modifica la reseña correspondiente al id con nuevos atributos
    @staticmethod
    async def updateReview(id:str, review: Review):
        _review = await database.get_collection('reviews').find_one({"_id":id})
        _review["reviewer_id"] = review.reviewer_id
        _review["driver_id"] = review.driver_id
        _review["rating"] = review.rating
        _review["comment"] = review.comment
        _review["date"] = review.date
        await database.get_collection('reviews').update_one({"_id":id}, {"$set":_review})
        
    # deleteReview(id: str): elimina la reseña correspondiente al id 
    @staticmethod
    async def deleteReview(id:str):
        await database.get_collection('reviews').delete_one({"_id":id})
        
    # reviewExists(id: str): comprueba si la reseña correspondiente al id existe en la base de datos
    @staticmethod
    async def reviewExists(id: str):
        _review = await database.get_collection('reviews').find_one({"_id":id})
        return _review is not None
    
class TripRepo():
    # getTrips(): devuelve todos los viajes en la base de datos
    @staticmethod
    async def getTrips():
        _trips = []
        collection = database.get_collection('trips').find()
        async for trip in collection:
            print(trip)
            _trips.append(trip)
        return _trips
    
    # getTripsById(id:str): devuelve el viaje correspondiente al identificador
    @staticmethod
    async def getTripById(id:str):
        return await database.get_collection('trips').find_one({"_id":id})
    
    # getTripsByUser(trip_id:str): devuelve todos los viajes de un usuario
    @staticmethod
    async def getTripsByUser(user_id:str):
        _trips = []
        collection = database.get_collection('trips').find({"driver_id":user_id})
        async for trip in collection:
            _trips.append(trip)
        return _trips
    
    # addTrip(trip: Trip): añade un viaje a la base de datos
    @staticmethod
    async def addTrip(trip: Trip):
        id = str(uuid.uuid4())
        _trip = {
            "_id": id,
            "driver_id": trip.driver_id,
            "start_location": trip.start_location,
            "departure_time": trip.departure_time,
            "available_places": trip.available_places,
            "price": trip.price,
            "trip_type": trip.trip_type,
            "day": trip.day,
            "end_date": trip.end_date,
            "arrival_location": trip.arrival_location,
        }
        await database.get_collection('trips').insert_one(_trip)
        
    # updateTrip(id: str, trip: Trip): modifica el viaje correspondiente al id con nuevos atributos
    @staticmethod
    async def updateTrip(id:str, trip: Trip):
        _trip = await database.get_collection('trips').find_one({"_id":id})
        _trip["driver_id"] = trip.driver_id
        _trip["start_location"] = trip.start_location
        _trip["departure_time"] = trip.departure_time
        _trip["available_places"] = trip.available_places
        _trip["price"] = trip.price
        _trip["trip_type"] = trip.trip_type
        _trip["day"] = trip.day
        _trip["end_date"] = trip.end_date
        _trip["arrival_location"] = trip.arrival_location
        await database.get_collection('trips').update_one({"_id":id}, {"$set":_trip})
        
    # deleteTrip(id: str): elimina el viaje correspondiente al id 
    @staticmethod
    async def deleteTrip(id:str):
        await database.get_collection('trips').delete_one({"_id":id})
        
    # tripExists(id: str): comprueba si el viaje correspondiente al id existe en la base de datos
    @staticmethod
    async def tripExists(id: str):
        _trip = await database.get_collection('trips').find_one({"_id":id})
        return _trip is not None

class UserRepo():
    # getUsers(): devuelve todos los usuarios en la base de datos
    @staticmethod
    async def getUsers():
        _users = []
        collection = database.get_collection('users').find()
        async for user in collection:
            _users.append(user)
        return _users
    
    # getUsersByName(name_substring: str): devuelve los usuarios cuyo nombre contiene el substring
    @staticmethod
    async def getUsersByName(name_substring: str):
        _users = []
        collection = database.get_collection('users').find({'name': {'$regex': f'.*{name_substring}.*'}})
        async for user in collection:
            _users.append(user)
        return _users
    
    # getUserId(id: str): devuelve el usuario correspondiente al identificador
    @staticmethod
    async def getUserId(id: str):
        return await database.get_collection('users').find_one({"_id":id})

    # addUser(user: User): añade un usuario a la base de datos
    @staticmethod
    async def addUser(user: User):
        id = str(uuid.uuid4())
        _user = {
            "_id":id,
            "name": user.name,
            "last_name": user.last_name,
            "bio": user.bio,
            "password": user.password,
            "email_address": user.email_address,
            "municipality": user.municipality,
            "zip_code": user.zip_code
        }
        await database.get_collection('users').insert_one(_user)
        
    # updateUser(id: str, user: User): modifica el usuario correspondiente al id con nuevos atributos
    @staticmethod
    async def updateUser(id: str, user: User):
        _user = await database.get_collection('users').find_one({"_id":id})
        _user["name"] = user.name
        _user["last_name"] = user.last_name
        _user["bio"] = user.bio
        _user["password"] = user.password
        _user["email_address"] = user.email_address
        _user["municipality"] = user.municipality
        _user["zip_code"] = user.zip_code
        await database.get_collection('users').update_one({"_id":id}, {"$set":_user})
        
    # deleteUser(id: str): elimina el usuario correspondiente al id 
    @staticmethod
    async def deleteUser(id:str):
        await database.get_collection('users').delete_one({"_id":id})
        
    # userExists(id: str): comprueba si el usuario correspondiente al id existe en la base de datos
    @staticmethod
    async def userExists(id: str):
        user = await database.get_collection('users').find_one({"_id":id})
        return user is not None
