from fastapi import APIRouter, HTTPException, Depends, Header
from bson import ObjectId
from datetime import datetime
from database import users_collection
from models import SignupModel, LoginModel
from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token, decode_token

router = APIRouter()

# ---------------------------
# SIGNUP
# ---------------------------
@router.post("/signup")
def signup(data: SignupModel):

    if users_collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(data.password)

    user_doc = {
        "name": data.name,
        "email": data.email,
        "gender": data.gender,
        "password": hashed_pw,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user_doc)

    return {"message": "User created", "user_id": str(result.inserted_id)}


# ---------------------------
# LOGIN
# ---------------------------
@router.post("/login")
def login(data: LoginModel):

    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    })

    return {"message": "Login successful", "token": token}


# ---------------------------
# AUTH MIDDLEWARE
# ---------------------------
def get_current_user(authorization: str = Header(None)):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split(" ")[1]

    try:
        payload = decode_token(token)
        user = users_collection.find_one({"_id": ObjectId(payload["user_id"])})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ---------------------------
# PROTECTED ROUTE
# ---------------------------
@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "name": user["name"],
        "email": user["email"],
        "gender": user["gender"]
    }
