from fastapi import APIRouter
from repository import BookingRepo, MessageRepo, ReviewRepo, TripRepo, UserRepo
from model import Booking, Message, Review, Trip, User, Response

"""
router.py: Contiene los métodos get, create, update y delete
"""

router = APIRouter(prefix="/BlaBlaETSIINF")

# BOOKING METHODS---------------------------------------------------------------------------------------------------------------

@router.get("/users/{user_id}/bookings/{id}")
async def get_id_booking(user_id: str, id: str):
    _booking = await BookingRepo.getBookingById(id)
    if not _booking or _booking["user_id"] != user_id:
        return Response(code=404, status="Not found", message=f"No booking found with id {id} for user {user_id}").dict(exclude_none=True)
    return Response(code=200, status="Ok", message="Success retrieving data from booking", result=_booking).dict(exclude_none=True)

@router.get("/users/{user_id}/bookings/")
async def get_user_bookings(user_id: str):
    _bookingList = await BookingRepo.getBookingsByUser(user_id)
    if len(_bookingList) == 0:
        return Response(code=404,status="Not found",message=f"No bookings found").dict(exclude_none=True)
    return Response(code=200,status="Ok",message="Success retrieving data from bookings", result=_bookingList).dict(exclude_none=True)

@router.put("/users/{user_id}/bookings/")
async def create_booking(user_id: str, booking: Booking):
    # Comprueba que el usuario de la reserva es correcto
    if not user_id == booking.user_id:
          return Response(code=400,status="Bad Request",message="The users don't match").dict(exclude_none=True)  
    # Comprueba que existe el usuario
    user_exists = await UserRepo.userExists(user_id)
    if not user_exists:
        return Response(code=400,status="Bad Request",message="Unknown user").dict(exclude_none=True)
    # Comprueba que existe el viaje
    trip_exists = await TripRepo.tripExists(booking.trip_id)
    if not trip_exists:
        return Response(code=400,status="Bad Request",message="Unknown trip").dict(exclude_none=True)
    # El estado debe ser ["accepted", "denied" o "pending"]
    if not booking.status in ["accepted", "denied", "pending"]:
        return Response(code=400,status="Bad Request",message="Incorrect status value").dict(exclude_none=True)
    await BookingRepo.addBooking(booking)
    return Response(code=200,status="Ok",message="Success saving data").dict(exclude_none=True)

@router.put("/users/{user_id}/bookings/{id}")
async def update_booking(user_id: str, id: str, booking: User):
    # Comprueba que el usuario de la reserva es correcto
    if not user_id == booking.user_id:
          return Response(code=400,status="Bad Request",message="The users don't match").dict(exclude_none=True)  
    # Comprueba que existe la reserva
    booking_exists = await BookingRepo.bookingExists(id)
    if not booking_exists:
        return Response(code=404,status="Not found",message=f"No booking with id {id} found").dict(exclude_none=True)
    # Comprueba que existe el usuario
    user_exists = await UserRepo.userExists(user_id)
    if not user_exists:
        return Response(code=400,status="Bad Request",message="Unknown user").dict(exclude_none=True)
    # Comprueba que existe el viaje
    trip_exists = await TripRepo.tripExists(booking.trip_id)
    if not trip_exists:
        return Response(code=400,status="Bad Request",message="Unknown trip").dict(exclude_none=True)
    # El estado debe ser ["accepted", "denied" o "pending"]
    if not booking.status in ["accepted", "denied", "pending"]:
        return Response(code=400,status="Bad Request",message="Incorrect status value").dict(exclude_none=True)
    await BookingRepo.updateBooking(id, booking)
    return Response(code=200,status="Ok",message="Success updating data").dict(exclude_none=True)

@router.delete("/users/{user_id}/bookings/{id}")
async def delete_booking(user_id: str, id: str):
    booking_exists = await BookingRepo.bookingExists(id)
    if not booking_exists:
        return Response(code=404,status="Not found",message=f"No booking with id {id} found").dict(exclude_none=True)
    await BookingRepo.deleteBooking(id)
    return Response(code=200,status="Ok",message="Success deleting data").dict(exclude_none=True)

# MESSAGE METHODS---------------------------------------------------------------------------------------------------------------

@router.get("/users/{user_id}/messages/{id}")
async def get_id_message(user_id: str, id: str):
    _message = await MessageRepo.getMessageById(id)
    if not _message or _message["user_id"] != user_id:
        return Response(code=404, status="Not found", message=f"No message found with id {id} for user {user_id}").dict(exclude_none=True)
    return Response(code=200, status="Ok", message="Success retrieving data from message", result=_message).dict(exclude_none=True)

@router.get("/users/{user_id}/messages/")
async def get_recipient_messages(user_id: str):
    _receivedMessages = await MessageRepo.getMessagesByRecipient(user_id)
    _sentMessages = await MessageRepo.getMessagesBySender(user_id)
    _messageList = list(_receivedMessages) + _sentMessages
    if len(_messageList) == 0:
        return Response(code=404,status="Not found",message=f"No messages found").dict(exclude_none=True)
    return Response(code=200,status="Ok",message="Success retrieving data from messages", result=_messageList).dict(exclude_none=True)

@router.put("/users/{user_id}/messages/")
async def create_message(user_id: str, message: Message):
    # Comprueba que el usuario de la reserva es correcto
    if not user_id == message.user_id:
          return Response(code=400,status="Bad Request",message="The users don't match").dict(exclude_none=True)  
    # Comprueba que existe el receptor
    recipient_exists = await UserRepo.userExists(message.recipient_id)
    if not recipient_exists:
        return Response(code=400,status="Bad Request",message="Unknown recipient").dict(exclude_none=True)
    # Comprueba que existe el emisor
    sender_exists = await TripRepo.tripExists(message.sender_id)
    if not sender_exists:
        return Response(code=400,status="Bad Request",message="Unknown sender").dict(exclude_none=True)
    await MessageRepo.addMessage(message)
    return Response(code=200,status="Ok",message="Success saving data").dict(exclude_none=True)

@router.delete("/users/{user_id}/messages/{id}")
async def delete_message(user_id: str, id: str):
    message_exists = await MessageRepo.messageExists(id)
    if not message_exists:
        return Response(code=404,status="Not found",message=f"No message with id {id} found").dict(exclude_none=True)
    await MessageRepo.deleteMessage(id)
    return Response(code=200,status="Ok",message="Success deleting data").dict(exclude_none=True)

# REVIEW METHODS----------------------------------------------------------------------------------------------------------------

@router.get("/users/{user_id}/reviews/{id}")
async def get_id_review(user_id: str, id: str):
    _review = await ReviewRepo.getReviewById(id)
    if not _review or _review["user_id"] != user_id:
        return Response(code=404, status="Not found", message=f"No review found with id {id} for user {user_id}").dict(exclude_none=True)
    return Response(code=200, status="Ok", message="Success retrieving data from review", result=_review).dict(exclude_none=True)

@router.get("/users/{user_id}/reviews/")
async def get_user_reviews(user_id: str):
    _reviewList = await ReviewRepo.getReviewsByUser(user_id)
    if len(_reviewList) == 0:
        return Response(code=404,status="Not found",message=f"No reviews found").dict(exclude_none=True)
    return Response(code=200,status="Ok",message="Success retrieving data from reviews", result=_reviewList).dict(exclude_none=True)

@router.put("/users/{user_id}/reviews/")
async def create_review(user_id: str, review: Review):
    # Comprueba que el usuario de la reseña es correcto
    if not user_id == review.driver_id:
          return Response(code=400,status="Bad Request",message="The users don't match").dict(exclude_none=True)  
    # Comprueba que existe el usuario
    user_exists = await UserRepo.userExists(user_id)
    if not user_exists:
        return Response(code=400,status="Bad Request",message="Unknown user").dict(exclude_none=True)
    # Comprueba que existe el viaje
    reviewer_exists = await UserRepo.userExists(review.reviewer_id)
    if not reviewer_exists:
        return Response(code=400,status="Bad Request",message="Unknown reviewer").dict(exclude_none=True)
    # El estado debe ser ["accepted", "denied" o "pending"]
    if not review.rating in [1, 2, 3, 4, 5]:
        return Response(code=400,status="Bad Request",message="Incorrect rating value").dict(exclude_none=True)
    await ReviewRepo.addReview(review)
    return Response(code=200,status="Ok",message="Success saving data").dict(exclude_none=True)

@router.put("/users/{user_id}/reviews/{id}")
async def update_review(user_id: str, id: str, review: User):
    # Comprueba que existe la reseña
    review_exists = await ReviewRepo.reviewExists(id)
    if not review_exists:
        return Response(code=400,status="Bad Request",message="Unknown review").dict(exclude_none=True)
    # Comprueba que el usuario de la reseña es correcto
    if not user_id == review.driver_id:
          return Response(code=400,status="Bad Request",message="The users don't match").dict(exclude_none=True)  
    # Comprueba que existe el usuario
    user_exists = await UserRepo.userExists(user_id)
    if not user_exists:
        return Response(code=400,status="Bad Request",message="Unknown user").dict(exclude_none=True)
    # Comprueba que existe el viaje
    reviewer_exists = await UserRepo.userExists(review.reviewer_id)
    if not reviewer_exists:
        return Response(code=400,status="Bad Request",message="Unknown reviewer").dict(exclude_none=True)
    # El estado debe ser ["accepted", "denied" o "pending"]
    if not review.rating in [1, 2, 3, 4, 5]:
        return Response(code=400,status="Bad Request",message="Incorrect rating value").dict(exclude_none=True)
    await ReviewRepo.updateReview(id, review)
    return Response(code=200,status="Ok",message="Success updating data").dict(exclude_none=True)

@router.delete("/users/{user_id}/reviews/{id}")
async def delete_review(user_id: str, id: str):
    review_exists = await UserRepo.userExists(id)
    if not review_exists:
        return Response(code=404,status="Not found",message=f"No review with id {id} found").dict(exclude_none=True)
    await ReviewRepo.deleteReview(id)
    return Response(code=200,status="Ok",message="Success deleting data").dict(exclude_none=True)

# TRIP METHODS------------------------------------------------------------------------------------------------------------------

@router.get("/trips/")
async def get_all_trips(driver_id: str):
    # Si incluye un substring, debera buscar viajes con conductores que lo incluyan en su nombre
    if(driver_id):
        _tripList = await TripRepo.getTripsByUser(driver_id)
    # Si no, devuelve todos los usuarios
    else:
        _tripList = await TripRepo.getTrips()
    if len(_tripList)==0:
        return Response(code=404,status="Not found",message=f"No trips found").dict(exclude_none=True)
    return Response(code=200,status="Ok",message="Success retrieving all data", result=_tripList).dict(exclude_none=True)

@router.get("/trips/{id}") 
async def get_id_trip(id:str):
    _trip = await TripRepo.getTripById(id)
    if not _trip:
        return Response(code=404,status="Not found",message=f"No trips found").dict(exclude_none=True)
    return Response(code=200,status="Ok",message="Success retrieving data from trip", result=_trip).dict(exclude_none=True)

@router.put("/trips/")
async def create_trip(trip: Trip):
    await TripRepo.addTrip(trip)
    return Response(code=200,status="Ok",message="Success saving data").dict(exclude_none=True)

@router.put("/trips/{id}")
async def update_trip(id: str, trip: Trip):
    trip_exists = await TripRepo.tripExists(id)
    if not trip_exists:
        return Response(code=404,status="Not found",message=f"No trip with id {id} found").dict(exclude_none=True)
    await TripRepo.updateTrip(id, trip)
    return Response(code=200,status="Ok",message="Success updating data").dict(exclude_none=True)

@router.delete("/trips/{id}")
async def delete_trip(id:str):
    trip_exists = await TripRepo.tripExists(id)
    if not trip_exists:
        return Response(code=404,status="Not found",message=f"No trip with id {id} found").dict(exclude_none=True)
    # Borra las reservas del viaje
    _bookingList = await BookingRepo.getBookingsByTrip(id)
    for booking in _bookingList:
        await BookingRepo.deleteBooking(booking["_id"])
    # Borra el viaje
    await TripRepo.deleteTrip(id)
    return Response(code=200,status="Ok",message="Success deleting data").dict(exclude_none=True)

# USER METHODS------------------------------------------------------------------------------------------------------------------

@router.get("/users/")
async def get_all_users(substring: str = None):
    # Si incluye un substring, debera buscar usuarios que lo incluyan en su nombre
    if(substring):
        _userList = await UserRepo.getUsersByName(substring)
    # Si no, devuelve todos los usuarios
    else:
        _userList = await UserRepo.getUsers()
    if len(_userList)==0:
        return Response(code=404,status="Not found",message=f"No users found").dict(exclude_none=True)
    return Response(code=200,status="Ok",message="Success retrieving all data", result=_userList).dict(exclude_none=True)

@router.get("/users/{id}") 
async def get_id_user(id:str):
    _user = await UserRepo.getUserId(id)
    if not _user:
        return Response(code=404,status="Not found",message=f"No users found").dict(exclude_none=True)
    return Response(code=200,status="Ok",message="Success retrieving data from user", result=_user).dict(exclude_none=True)

@router.put("/users/")
async def create_user(user: User):
    await UserRepo.addUser(user)
    return Response(code=200,status="Ok",message="Success saving data").dict(exclude_none=True)

@router.put("/users/{id}")
async def update_user(id: str, user: User):
    user_exists = await UserRepo.userExists(id)
    if not user_exists:
        return Response(code=404,status="Not found",message=f"No user with id {id} found").dict(exclude_none=True)
    await UserRepo.updateUser(id, user)
    return Response(code=200,status="Ok",message="Success updating data").dict(exclude_none=True)

@router.delete("/users/{id}")
async def delete_user(id:str):
    user_exists = await UserRepo.userExists(id)
    if not user_exists:
        return Response(code=404,status="Not found",message=f"No user with id {id} found").dict(exclude_none=True)
    # Borra las reservas del usuario
    _bookingList = await BookingRepo.getBookingsByUser(id)
    for booking in _bookingList:
        await BookingRepo.deleteBooking(booking["_id"])
    # Borra las reseñas del usuario
    _reviewList = await ReviewRepo.getReviewsByUser(id)
    for review in _reviewList:
        await ReviewRepo.deleteReview(booking["_id"])
    # Borra los viajes del usuario
    _tripList = await TripRepo.getTripsByUser(id)
    for trip in _tripList:
        await TripRepo.deleteTrip(trip["_id"])
    # Borra el usuario
    await UserRepo.deleteUser(id)
    return Response(code=200,status="Ok",message="Success deleting data").dict(exclude_none=True)