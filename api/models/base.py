from sqlmodel import SQLModel, Field, select, Session, delete
from typing import Optional, Type, TypeVar, Sequence, Generic
from sqlalchemy.orm import selectinload
from contextlib import contextmanager
from db import engine
from datetime import datetime, UTC


T = TypeVar("T", bound="Base")


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session


class Base(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(UTC))
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @classmethod
    def __get_query(cls: Type[T], sess: Session | None = None):
        """Always return a QueryBuilder with a valid session."""
        if sess is not None:
            return QueryBuilder(cls, sess)
        # create a temporary session (caller doesn’t pass one)
        return QueryBuilder(cls, Session(engine))

    # Main query builder helper
    @classmethod
    def query(cls: Type[T], sess: Session | None = None):
        return cls.__get_query(sess).where(cls.deleted_at == None)

    # Helper for service layer
    @classmethod
    def find_by_id(cls: Type[T], id: int, sess: Session | None = None) -> Optional[T]:
        return cls.query(sess).where(cls.id == id).first()
    
    # CRUD shortcut dùng QueryBuilder
    @classmethod
    def create(cls: Type[T], data: SQLModel | dict, sess: Session | None = None) -> T:
        return cls.query(sess).create(data)

    @classmethod
    def create_many(cls: Type[T], data_list: list[SQLModel] | list[dict], sess: Session | None = None):
        return cls.query(sess).create_many(data_list)

    @classmethod
    def update(cls: Type[T], id: int, data: SQLModel | dict, sess: Session | None = None):
        return cls.query(sess).where(cls.id == id).update(data)

    @classmethod
    def update_many(cls: Type[T], filters: list, data: dict, sess: Session | None = None):
        return cls.query(sess).where(*filters).update_many(data)

    @classmethod
    def delete_soft(cls: Type[T], id, sess: Session | None = None):
        return cls.query(sess).where(cls.id == id).update({"deleted_at": datetime.now(UTC)})
    
    @classmethod
    def delete_hard(cls: Type[T], id, sess: Session | None = None):
        return cls.query(sess).where(cls.id == id).delete()


class QueryBuilder(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
        self._filters = []
        self._options = []

    # where()
    def where(self, *conditions):
        self._filters.extend(conditions)
        return self

    # with_() → eager load quan hệ
    def with_(self, *relations: str):
        for rel in relations:
            self._options.append(selectinload(getattr(self.model, rel)))
        return self

    # where_has() → lọc theo quan hệ (giống whereHas trong Eloquent)
    def where_has(self, relation: str, condition_func):
        rel_model = getattr(self.model, relation).property.mapper.class_
        subquery = condition_func(rel_model)
        self._filters.append(getattr(self.model, relation).any(subquery))
        return self
    
    # ---- CRUD ----

    def create(self, data: SQLModel | dict) -> T:
        payload = data.model_dump() if isinstance(data, SQLModel) else data
        instance = self.model(**payload)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def create_many(self, data_list: list[SQLModel] | list[dict]) -> list[T]:
        if not data_list:
            return []
        instances: list[T] = []
        for item in data_list:
            instance = self.model(**(item.model_dump() if isinstance(item, SQLModel) else item))
            instances.append(instance)
        self.session.add_all(instances)
        self.session.commit()
        for inst in instances:
            self.session.refresh(inst)
        return instances

    def update(self, data: SQLModel | dict ) -> Optional[T]:
        payload = data.model_dump() if isinstance(data, SQLModel) else data
        stmt = select(self.model).where(*self._filters)
        obj = self.session.exec(stmt).first()
        if not obj:
            return None
        for key, value in payload.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.updated_at = datetime.now(UTC)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update_many(self, data: dict) -> int:
        stmt = select(self.model).where(*self._filters)
        results = self.session.exec(stmt).all()
        for obj in results:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            obj.updated_at = datetime.now(UTC)
        self.session.commit()
        return len(results)
    
    def delete(self) -> Optional[T]:
        obj = self.session.exec(select(self.model).where(*self._filters)).first()
        if not obj:
            return None
        self.session.delete(obj)
        self.session.commit()
        return obj

    def delete_many(self) -> int:
        stmt = delete(self.model).where(*self._filters)
        result = self.session.exec(stmt)
        self.session.commit()
        return result.rowcount or 0
    # ---- Query ----

    # all()
    def all(self) -> Sequence[T]:
        stmt = select(self.model)
        if self._filters:
            stmt = stmt.where(*self._filters)
        if self._options:
            stmt = stmt.options(*self._options)
        return self.session.exec(stmt).all()

    # first()
    def first(self) -> Optional[T]:
        stmt = select(self.model)
        if self._filters:
            stmt = stmt.where(*self._filters)
        if self._options:
            stmt = stmt.options(*self._options)
        return self.session.exec(stmt).first()