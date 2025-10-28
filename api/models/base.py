from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, Type, TypeVar, Sequence, Generic
from sqlalchemy.orm import selectinload
from contextlib import contextmanager
from db import engine


T = TypeVar("T", bound="Base")


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session


class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Main query builder helper
    @classmethod
    def find(cls: Type[T], sess: Session | None = None):
        sess = sess or Session(engine)
        return QueryBuilder(cls, sess)

    # Helper for service layer
    @classmethod
    def find_by_pk(cls: Type[T], pk: int):
        return cls.find().where(cls.id == pk).first()


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