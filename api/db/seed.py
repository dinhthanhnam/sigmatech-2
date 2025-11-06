from db import engine
from sqlmodel import Session, select
from models.user import User
from models.product import Product
from models.attribute import Attribute
from schemas.user import UserCreate, UserUpdate
from schemas.product import ProductCreate, LaptopCreate, MonitorCreate

def seed():
    with Session(engine) as session:
        try:
            Attribute.create_many(
                [
                    Attribute(name="model"),
                    Attribute(name="lap_size"),
                    Attribute(name="mon_size"),
                    Attribute(name="type")
                ], 
                session
            )
            User.create_many([
                    UserCreate(username="admin123", email="admin@example.com", password="12345678"),
                    UserCreate(username="user1234", email="user1@example.com", password="12345678"),
                ],
                session
            )
            Product.create(
                LaptopCreate(name="Laptop 1", lap_size="14inch", model="ASUS01", mon_size="14inch")
                ,session
            )
            Product.create(
                MonitorCreate(name="Monitor 1", model="ASUS01", mon_size="14inch")
                ,session
            )
            session.commit()
        except Exception as e:
            session.rollback()
            print("Seed failed:", e)

if __name__ == "__main__":
    seed()