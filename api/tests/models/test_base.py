from models.base import Base
from sqlmodel import SQLModel, Session, create_engine
import pytest

class Model(Base, table=True):
    __tablename__ = "models" # type: ignore

    name: str


@pytest.fixture(autouse=True)
def setup_db():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


def test_create(setup_db):
    user = Model.create({"name": "abc"}, sess=setup_db)
    setup_db.commit()
    setup_db.refresh(user)
    assert user.id is not None
    assert user.name == "abc"
    assert user.created_at is not None


def test_create_many(setup_db):
    users = Model.create_many(
        [
            {"name": "abc"},
            {"name": "abc"}
        ],
        sess=setup_db,
    )

    setup_db.commit() 
    for u in users:
        setup_db.refresh(u)
    assert len(users) == 2
    assert all(u.id is not None for u in users)
