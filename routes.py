# routes.py
from fastapi import APIRouter, HTTPException, Depends
from db import Session, engine, GroceryData, Cart, Order, OrderDetail
from sqlmodel import Session, select
from models import GroceryDataCreate, CartCreate, OrderCreate, CheckoutForm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_session():
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/product/{product_id}")
def get_product_by_id(product_id: int, session: Session = Depends(get_session)):
    product = session.get(GroceryData, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/cart/")
def add_to_cart(cart: CartCreate, session: Session = Depends(get_session)):
    # Validate the product_id
    product = session.get(GroceryData, cart.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_cart = Cart.from_orm(cart)
    try:
        session.add(db_cart)
        session.commit()
        session.refresh(db_cart)
        logger.info(f"Added to cart: {db_cart}")
        return db_cart
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding to cart: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add to cart: {str(e)}")

@router.post("/order/")
def order_now(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order.from_orm(order)
    try:
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        logger.info(f"Order placed: {db_order}")
        return db_order
    except Exception as e:
        session.rollback()
        logger.error(f"Error placing order: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to place order: {str(e)}")
@router.post("/checkout/")
def submit_checkout_form(checkout_data: CheckoutForm, session: Session = Depends(get_session)):
    order_detail = OrderDetail(
        order_id=1,  # This should be dynamically assigned based on actual order creation logic
        customer_name=checkout_data.name,
        customer_email=checkout_data.email,
        customer_address=checkout_data.home_address,
        customer_phone=checkout_data.phone_number,
        payment_method=checkout_data.payment_method
    )
    try:
        session.add(order_detail)
        session.commit()
        session.refresh(order_detail)
        return {"message": "Checkout successful", "order_details": order_detail}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process checkout: {str(e)}")