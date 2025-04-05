from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# API Models
class ProductCreate(BaseModel):
    name: str
    price: int

class CartItem(BaseModel):
    product_id: int
    quantity: int

cart = []

@app.get("/products", response_model=List[ProductCreate])
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.post("/add-to-cart")
def add_to_cart(item: CartItem):
    cart.append(item)
    return {"message": "Item added to cart", "cart": cart}

@app.post("/checkout")
def checkout():
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    total = sum([item.quantity * 10 for item in cart])  # Assuming price=10 for simplicity
    cart.clear()
    return {"message": "Order placed successfully", "total": total}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
