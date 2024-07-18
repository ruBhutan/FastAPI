from fastapi import FastAPI
from app.auth import create_access_token, get_current_user
from app.models import User, Product
from app.crud import register_user, login_user, create_product, list_products
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(register_user.router)
app.include_router(login_user.router)
app.include_router(create_product.router)
app.include_router(list_products.router)

if __name__ == "__main__":
    app.run(debug=True)
