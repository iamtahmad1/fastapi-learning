from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
import jwt
import datetime
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

app = FastAPI()

# Secret key for signing JWT
SECRET_KEY = "mysecretkey"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {}

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


#########################

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash and store password
    hashed_password = hash_password(user.password)
    users_db[user.username] = {"password": hashed_password}
    
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    if user.username not in users_db:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    
    print(users_db)
    stored_password = users_db[user.username]["password"]

    if not verify_password(user.password, stored_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create JWT payload
    payload = {
        "sub": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}

###########
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to extract user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")

        if username not in users_db:
            raise HTTPException(status_code=401, detail="Invalid user")

        return username

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Protected endpoint
@app.get("/tasks")
def get_tasks(user: str = Depends(get_current_user)):
    
    return {"message": f"Welcome {user}, here are your tasks!"}