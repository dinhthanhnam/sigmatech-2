from sqlmodel import Session, select
from models.user import User
from models.product import Product
from models.attribute import Attribute
from schemas.user import UserCreate, UserUpdate
from schemas.product import ProductCreate, LaptopCreate, MonitorCreate
from db import transactional

@transactional
def seed():
    Attribute.create_many(
        [
            Attribute(name="model"),
            Attribute(name="lap_size"),
            Attribute(name="mon_size"),
            Attribute(name="type")
        ]
    )
    User.create_many([
            UserCreate(username="nextserver", email="nextserver@internal.dev", password="12345678", is_superuser=True),
            UserCreate(username="admin123", email="admin@example.com", password="12345678", is_superuser=True),
            UserCreate(username="user1234", email="user1@example.com", password="12345678"),
        ]
    )
    Product.create(
        LaptopCreate(name="Laptop 1", lap_size="14inch", model="ASUS01", mon_size="14inch")
    )
    Product.create(
        MonitorCreate(name="Monitor 1", model="ASUS01", mon_size="14inch")
    )
if __name__ == "__main__":
    seed()