import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, Order


# Setup an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database and tables
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(setup_database):
    # Create a new session for a test
    session = SessionLocal()
    yield session
    session.close()

def test_create_customer(db_session):
    # Test creating a new customer
    new_customer = Customer(name="Jane Doe", email="jane@example.com", phone_number="+254711111111")
    db_session.add(new_customer)
    db_session.commit()
    
    customer_in_db = db_session.query(Customer).filter_by(email="jane@example.com").first()
    assert customer_in_db is not None
    assert customer_in_db.name == "Jane Doe"

def test_create_order(db_session):
    # Test creating a new order associated with a customer
    customer = Customer(name="John Doe", email="john@example.com", phone_number="+254722222222")
    db_session.add(customer)
    db_session.commit()

    new_order = Order(item="Laptop", amount=1, customer_id=customer.id)
    db_session.add(new_order)
    db_session.commit()

    order_in_db = db_session.query(Order).filter_by(item="Laptop").first()
    assert order_in_db is not None
    assert order_in_db.customer_id == customer.id
