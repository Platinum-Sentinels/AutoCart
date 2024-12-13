from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Initialize FastAPI app
app = FastAPI()

# JWT Secret and Algorithm
SECRET_KEY = "your_jwt_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock user database
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "User One",
        "email": "user1@example.com",
        "hashed_password": "$2b$12$KIXa.CS0Q.O/4bx6/zGyXuj/m6tuwQdxzMgKzNkbMdBOmMiRZ6ie6",  # "password"
        "disabled": False,
    }
}

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class SearchQuery(BaseModel):
    keyword: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None

class Product(BaseModel):
    name: str
    price: float
    rating: float
    link: str

# Mock product database
products_db = [
    {"name": "iPhone 15", "price": 999.99, "rating": 4.8, "link": "https://example.com/iphone15"},
    {"name": "Galaxy S23", "price": 799.99, "rating": 4.5, "link": "https://example.com/galaxys23"},
    {"name": "Laptop Charger", "price": 50.0, "rating": 4.2, "link": "https://example.com/charger"},
]

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    user = db.get(username)
    if user:
        return UserInDB(**user)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return get_user(fake_users_db, username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/search", response_model=List[Product])
def search_products(query: SearchQuery):
    results = products_db

    if query.keyword:
        results = [p for p in results if query.keyword.lower() in p["name"].lower()]

    if query.min_price is not None:
        results = [p for p in results if p["price"] >= query.min_price]

    if query.max_price is not None:
        results = [p for p in results if p["price"] <= query.max_price]

    if query.min_rating is not None:
        results = [p for p in results if p["rating"] >= query.min_rating]

    if query.max_rating is not None:
        results = [p for p in results if p["rating"] <= query.max_rating]

    return results
