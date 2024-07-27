# db.py
from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional

# Database URL
DATABASE_URL = "postgresql://neondb_owner:kz7jBqK5RQNM@ep-flat-snow-a59h4e3g.us-east-2.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class GroceryData(SQLModel, table=True):
    __tablename__ = "grocery_data"
    product_id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    sub_category: str
    product_name: str
    price: float
    image_url: str

class Cart(SQLModel, table=True):
    __tablename__ = "cart"
    cart_id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    quantity: int

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    order_id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int
    total_price: float
    order_status: str

class OrderDetail(SQLModel, table=True):
    detail_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int  # This should link to an existing order
    customer_name: str
    customer_email: str
    customer_address: str
    customer_phone: str
    payment_method: str

# Ensure that this function is actually being called
if __name__ == "__main__":
    create_db_and_tables()
