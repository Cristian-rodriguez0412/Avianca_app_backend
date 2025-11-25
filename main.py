from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Avianca Connect FastAPI")

@app.get("/api/status")
def status():
    return {"service":"Avianca Connect API","status":"online","version":"1.0"}

@app.get("/api/flights/search")
def search(from_: str = None, to: str = None, date: str = None):
    # fastapi treats 'from' as reserved, using from_
    if not from_ or not to or not date:
        raise HTTPException(status_code=400, detail="Missing parameters: from,to,date")
    flights = [
        {"flight_number":"AV101","from":from_,"to":to,"date":date,"departure":"08:00","arrival":"09:15","price_usd":120},
        {"flight_number":"AV202","from":from_,"to":to,"date":date,"departure":"13:00","arrival":"14:10","price_usd":98}
    ]
    return {"status":"success","results":flights}

class Booking(BaseModel):
    flight_number: str
    user_id: str

@app.post("/api/flights/book")
def book(booking: Booking):
    return {"status":"success","booking":{"booking_id":"BK12345","flight_number":booking.flight_number,"user_id":booking.user_id}}

class RegisterModel(BaseModel):
    name:str
    email:str
    password:str

@app.post("/api/auth/register")
def register(body: RegisterModel):
    return {"status":"success","message":"User registered","user":{"id":"USR123","name":body.name,"email":body.email}}

class LoginModel(BaseModel):
    email:str
    password:str

@app.post("/api/auth/login")
def login(body: LoginModel):
    return {"status":"success","token":"TOKEN_FAKE_123456","user":{"id":"USR123","email":body.email}}

@app.get("/api/user/profile")
def profile():
    return {"id":"USR123","name":"John Doe","email":"john.doe@example.com","miles":4300,"tier":"Silver"}

@app.get("/api/user/miles")
def miles():
    return {"status":"success","miles":{"available":4300,"pending":1200,"last_update":"2025-01-22"}}
