from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import List
import re

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str = Field(..., description="Kenyan phone number format: +254 followed by 9 digits", example="+254727284935")

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        if not re.match(r'^\+254\d{9}$', v):
            raise ValueError('Invalid Kenyan phone number format')
        return v

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    item: str
    amount: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    order_time: datetime
    customer_id: int

    class Config:
        from_attributes = True

class CustomerWithOrders(Customer):
    orders: List[Order] = []

class OrderWithCustomer(Order):
    customer: Customer