from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)  # Stored as string to preserve the '+254' prefix
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String)
    amount = Column(Float)
    order_time = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="orders")