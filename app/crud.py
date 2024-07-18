from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.auth import create_access_token, get_current_user
from app.models import User, Product
from app.schemas import UserCreate, UserLogin, ProductCreate
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=User)
async def register_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = await User.create(username=user.username, password_hash=hashed_password)
    return new_user


@router.post("/login", response_model=Token)
async def login_user(user: UserLogin):
    user_obj = await User.filter(username=user.username).first()
    if not user_obj:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(user.password, user_obj.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/products", response_model=List[Product])
async def list_products(current_user: User = Depends(get_current_user)):
    return await Product.all()


@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_user)):
    new_product = await Product.create(name=product.name, description=product.description)
    return new_product
