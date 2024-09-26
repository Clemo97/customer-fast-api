import os
import secrets
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from authentication import verify_token, get_token_from_code
from models import Base, Customer, Order
from schemas import CustomerCreate, CustomerWithOrders, OrderCreate, OrderWithCustomer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sms import send_sms

# Load environment variables
load_dotenv()

# Environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
API_AUDIENCE = os.getenv("API_AUDIENCE")
CALLBACK_URL = os.getenv("CALLBACK_URL")

app = FastAPI(
    title="Customer Order Documentation",  
    description="SIL API documentation",  
    version="1.0.0",  
    docs_url="/docs",  
    redoc_url="/redoc",  
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Database setup (using Supabase PostgreSQL instance)
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/login")
async def login():
    state = secrets.token_urlsafe(16)
    auth_url = f"https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri={CALLBACK_URL}&scope=openid profile email&audience={API_AUDIENCE}&state={state}"
    logger.info(f"Redirecting to Auth0: {auth_url}")
    return RedirectResponse(url=auth_url, status_code=303)

@app.get("/callback")
async def callback(code: str, state: str):
    logger.info(f"Received callback with code: {code[:10]}... and state: {state}")
    return get_token_from_code(code)

@app.get("/api/protected")
async def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "This is a protected endpoint", "user": payload.get("sub")}

@app.get("/api/public")
async def public_route():
    return {"message": "This is a public endpoint"}

# Customer endpoints
@app.post("/api/customers", response_model=CustomerWithOrders)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), payload: dict = Depends(verify_token)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/api/customers/{customer_id}", response_model=CustomerWithOrders)
async def read_customer(customer_id: int, db: Session = Depends(get_db), payload: dict = Depends(verify_token)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Order endpoints
@app.post("/api/orders", response_model=OrderWithCustomer)
async def create_order(order: OrderCreate, customer_id: int, db: Session = Depends(get_db), payload: dict = Depends(verify_token)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Create order
    db_order = Order(**order.dict(), customer_id=customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Send SMS confirmation to customer
    message = f"Dear {db_customer.name}, your order for {db_order.item} amounting to {db_order.amount} has been received."
    send_sms(db_customer.phone_number, message)

    return db_order

@app.get("/api/orders/{order_id}", response_model=OrderWithCustomer)
async def read_order(order_id: int, db: Session = Depends(get_db), payload: dict = Depends(verify_token)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)