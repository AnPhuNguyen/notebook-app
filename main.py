from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import user_utils as utils
import re
# ------------------------------initialize the app + user base models--------------------------------
app = FastAPI()

class LoginRequest(BaseModel):
    info: str #either username or email
    password: str

class signupRequest(BaseModel):
    username: str
    email: str
    password: str

from pydantic import BaseModel

class user(BaseModel):
    userId: int
    username: str
    email: str
    password: str

class note(BaseModel):
    noteId: int
    userId: int
    title: str
    note_content: str

# ---------------------------------- setup jwt -----------------------------------------

from datetime import datetime, timedelta, timezone
from typing import Optional

SECRET_KEY = "newbie"  # Thay thế bằng một khóa bí mật mạnh mẽ trong thực tế
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

import jwt
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        # datetime.utcnow() can no longer be used since it lacks timezone information
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ---------------------------------- API below -----------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# 1) login >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.get("/", response_class=FileResponse)
def root():
    return FileResponse("static/login.html")

@app.get("/login", response_class=FileResponse)
def login_page():
    return FileResponse("static/login.html")

@app.post("/login")
async def login(login_request: LoginRequest):
    # handle empty input in backend (if someone uses tool to run api directly)
    if not login_request.password: #if empty string, this will be false
        raise HTTPException(status_code=400, detail="Password is required",headers={"WWW-Authenticate": "Bearer"})
    if not login_request.info:
        raise HTTPException(status_code=400, detail="Username or email is required",headers={"WWW-Authenticate": "Bearer"})
    
    # validation ... (uses code 400 to properly deny request)
    inputUser = utils.getUser(login_request.info, login_request.password)
    if not inputUser:
        raise HTTPException(status_code=400, detail="User not found. Either username, email or password is incorrect")

    #creating jwt token
    tokenData = {
        "userId": inputUser.userId,
        "username": inputUser.username,
        "email": inputUser.email,
        "password": inputUser.password
    }
    access_token = create_access_token(data=tokenData)
    print(access_token)
    
    return {"message": "Login successful", "access_token": access_token}

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        email = payload.get("email")
        password = payload.get("password")
        exp = payload.get("exp")
        if (not username and not email) or password is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        # if exp < datetime.now():
        #     raise HTTPException(status_code=403, detail="Session expired. Try again later")
        
        # after successfully validating token, return user object (info will be either username or email)
        info: str
        if username:
            info = username
        elif email:
            info = email
        return utils.getUser(info, password)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@app.get("/users/me", response_model=user)
async def read_users_me(current_user: user = Depends(get_current_user)):
    return current_user

@app.post("/signup")
async def signup(signup_request: signupRequest):
    # handle empty input in backend (if someone uses tool to run api directly)
    if not signup_request.password:
        raise HTTPException(status_code=400, detail="Password is required")
    if not signup_request.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not signup_request.email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    #name, email max length = 50; password max length = 60
    #valid email example: a@hu.edu.vn; google@gmail.com
    if len(signup_request.username) > 50:
        raise HTTPException(status_code=400, detail="Username must be less than 50 characters")
    if len(signup_request.email) > 50:
        raise HTTPException(status_code=400, detail="Email must be less than 50 characters")
    if not isEmailValid(signup_request.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if len(signup_request.password) > 60:
        raise HTTPException(status_code=400, detail="Password must be less than 60 characters")
    
    utils.insertUser(signup_request.username, signup_request.email, signup_request.password)
    return {"message": "Signup successful. Please return to log in screen to actually log in"}

def isEmailValid(email:str):
    x = re.search(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', email) #use regex to check if email is valid
    return bool(x)

# 2) notebook >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.get("/user/me/main")
async def screen():
    return FileResponse("static/notebook_app.html")

if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    # format_date = datetime.strptime("1747793132", "%y-%m-%d %H:%M:%S")
    # print(format_date)
    # print(1747793132 < datetime.now())
    pass