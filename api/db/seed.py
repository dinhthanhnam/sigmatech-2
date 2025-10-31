from db import engine
from sqlmodel import Session, select
from models.user import User
from models.product import Product
from models.attribute import Attribute
from models.base import get_session
from schemas.user import UserCreate
from schemas.product import ProductCreate, LaptopCreate, MonitorCreate

def seed():
    with Session(engine) as session:
        try:
            Attribute.create_many(
                [
                    Attribute(name="model"),
                    Attribute(name="lap_size"),
                    Attribute(name="mon_size"),
                ], 
                session
            )
            User.create_many([
                    UserCreate(username="admin", email="admin@example.com", hashed_password="12345678"),
                    UserCreate(username="user1", email="user1@example.com", hashed_password="12345678"),
                ],
                session
            )
            Product.create(
                LaptopCreate(name="Laptop 1", lap_size="14inch", model="ASUS01", mon_size="14inch")
                ,session
            )
            session.commit()
        except Exception as e:
            session.rollback()
            print("Seed failed:", e)

if __name__ == "__main__":
    seed()