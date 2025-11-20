from models.base import Base
from sqlmodel import SQLModel, Session
import pytest
from typing import Optional
from db import clear_session, test_engine, get_session, set_session


class Model(Base, table=True):
    __tablename__ = "models" # type: ignore

    name: str
    brand: Optional[str] = None
    password: Optional[str] = None

@pytest.fixture(autouse=True)
def setup_db():
    set_session(Session(test_engine))
    SQLModel.metadata.drop_all(test_engine) 
    SQLModel.metadata.create_all(test_engine)
    yield
    clear_session()

def test_create():
    user = Model.create(Model(name='abc', brand='intel'))
    assert user.id is not None

def test_create_many():
    users = Model.create_many(
        [
            Model(name='abc', brand='intel'),
            Model(name='bcd', brand='intel')
        ]
    )

    sess = get_session()
    sess.commit()
    for u in users:
        sess.refresh(u)
    assert len(users) == 2
    assert all(u.id is not None for u in users)


def test_select_only():
    _ = Model.create(Model(name='abc', brand='intel'))
    result = Model.query().only(Model.id, Model.name).first()
    assert result != None
    assert result.name == "abc"


def test_update_one():
    _ = Model.create(Model(name='abc', brand='intel'))
    # result = Model.query().update()
    result = Model.update_one(1, Model(name='bcd', brand='intel'))
    assert result != None
    assert isinstance(result, Model)
    assert result.name == "bcd"


def test_update_many():
    _ = Model.create_many(
        [
            Model(name='abc', brand='intel'),
            Model(name='bcd', brand='intel')
        ])
    updated = Model.update_many(filters=[Model.brand == 'intel', Model.name == 'abc'], data={"name": "xyz"})
    assert updated != None
    print(updated)
    assert isinstance(updated, list)
    assert len(updated) == 1
    for item in updated:
        assert item.name == 'xyz'


def test_update_bulk():
    _ = Model.create_many(
        [
            Model(name='abc', brand='intel'),
            Model(name='bcd', brand='intel')
        ])
    updated = Model.update_bulk([{"id": "1","name": "xyz"},{"id": "2","brand": "asus"}])
    assert updated == 2
    updated_objs = Model.find_many(filters=[Model.id.in_([1,2])])
    assert updated_objs[0].name == "xyz"
    assert updated_objs[1].brand == "asus"