# models.py
from pydantic import BaseModel

class GroceryDataCreate(BaseModel):
    product_id: int
    category: str
    sub_category: str
    product_name: str
    price: float
    image_url: str

    class Config:
        orm_mode = True

class CartCreate(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    cart_id: int
    total_price: float
    order_status: str

    class Config:
        orm_mode = True
# models.py
# models.py
from pydantic import BaseModel, EmailStr, Field

class CheckoutForm(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    home_address: str
    phone_number: str = Field(..., min_length=10, max_length=15)
    payment_method: str = Field(..., pattern="^(cash on delivery|stripe)$")

    class Config:
        orm_mode = True
