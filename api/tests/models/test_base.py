from models.base import Base
from sqlmodel import SQLModel, Session, create_engine, MetaData, text
import pytest
from typing import Optional

test_metadata = MetaData()

class Model(Base, table=True, metadata=test_metadata):
    __tablename__ = "models" # type: ignore

    name: str

class PartialModel(Base, table=False):
    name: Optional[str]

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
            {"name": "bcd"}
        ],
        sess=setup_db,
    )

    setup_db.commit() 
    for u in users:
        setup_db.refresh(u)
    assert len(users) == 2
    assert all(u.id is not None for u in users)


def test_select(setup_db):
    _ = Model.create({"name": "abc"}, sess=setup_db)
    result = Model.query(sess=setup_db).only(Model.id, Model.name).first()
    assert result != None
    assert result.name == "abc"