from db import engine
from sqlmodel import Session, select
from models.user import User
from schemas.user import UserCreate

def seed():
    with Session(engine) as session:
        User.create(session, UserCreate(username="admin", email="admin@example.com", password="changeme"))

if __name__ == "__main__":
    seed()