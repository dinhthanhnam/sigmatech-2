from sqlmodel import SQLModel, Field, select, Session, delete, update, case
from sqlalchemy.orm import load_only
from pydantic import create_model, BaseModel
from typing import Optional, Type, TypeVar, Sequence, Generic, Literal, Union, cast
from sqlalchemy.orm import selectinload
from db import engine
from datetime import datetime, UTC
from sqlalchemy import ColumnElement
from db import get_session, engine, test_engine

T = TypeVar("T", bound="Base")


class Base(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(UTC))
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @classmethod
    def __get_session(cls):
        return get_session()

    @classmethod
    def __get_query(cls: Type[T]):
        """Always return a QueryBuilder with a valid session."""
        return QueryBuilder(cls, cls.__get_session())

    # Main query builder helper
    @classmethod
    def query(cls: Type[T]):
        return cls.__get_query().where(cls.deleted_at == None)

    # Helper for service layer
    @classmethod
    def find_by_id(cls: Type[T], id: int) -> Optional[T]:
        return cls.query().where(cls.id == id).first()
    
    # CRUD shortcut dùng QueryBuilder
    @classmethod
    def find_one(cls: Type[T], filters: list) -> Optional[T]:
        return cls.query().where(*filters).first()
    
    @classmethod
    def find_many(cls: Type[T], filters: list) -> Optional[Sequence[T]]:
        return cls.query().where(*filters).all()
    
    @classmethod
    def create(cls: Type[T], data: SQLModel | dict) -> T:
        return cls.query().create(data)
    
    @classmethod
    def create_many(cls: Type[T], data_list: list[SQLModel] | list[dict]) -> Sequence[T]:
        return cls.query().create_many(data_list)

    @classmethod
    def update_one(cls: Type[T], id: int, data: SQLModel | dict) -> Optional[T]:
        updated = cls.query().where(cls.id == id).update(data)
        if updated:
            return cast(T, updated[0])
        else:
            return None

    @classmethod
    def update_many(cls: Type[T], filters: list, data: dict) -> Optional[Sequence[T]]:
        return cls.query().where(*filters).update(data)

    @classmethod
    def update_bulk(cls: Type[T], data_list: list[SQLModel] | list[dict]) -> int:
        return cls.query().update_bulk(data_list)

    @classmethod
    def delete_soft(cls: Type[T], id) -> Optional[T]:
        deleted = cls.query().where(cls.id == id).update({"deleted_at": datetime.now(UTC)})
        if deleted:
            return cast(T, deleted[0])
        else:
            return None


    @classmethod
    def delete_hard(cls: Type[T], id):
        return cls.query().where(cls.id == id).delete()


class QueryBuilder(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self._columns: tuple[str, ...] | None = None
        self._filters = []
        self._options = []
        self._offset = None
        self._limit = None
        self._order_by = []
        self._group_by = []
        self.session = session
        self.auto_commit = True


    def _commit(self):
        if self.auto_commit and not self.session.in_transaction():
            self.session.commit()


    def only(self, *fields):
        self._options.append(load_only(*fields))
        return self


    # where()
    def where(self, *conditions):
        self._filters.extend(conditions)
        return self


    # offset -> lấy bắt đầu từ bản ghi số bao nhiêu
    def offset(self, value: int):
        self._offset = value
        return self

    # take -> lấy bao nhiêu 1 lần
    def limit(self, value: int):  # tương đương limit
        self._limit = value
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

    # order_by -> sắp xếp theo một hoặc nhiều cột
    def order_by(self, *columns):
        self._order_by = columns
        return self

    # group_by -> gom nhóm theo một hoặc nhiều cột
    def group_by(self, *columns):
        self._group_by = columns
        return self

    # ---- CRUD ----

    def create(self, data: SQLModel | dict) -> T:
        payload = data.model_dump() if isinstance(data, SQLModel) else data
        instance = self.model(**payload)
        self.session.add(instance)
        self.session.flush()
        self._commit()
        return instance

    def create_many(self, data_list: list[SQLModel] | list[dict]) -> Sequence[T]:
        if not data_list:
            return []
        instances: list[T] = []
        for item in data_list:
            instance = self.model(**(item.model_dump() if isinstance(item, SQLModel) else item))
            instances.append(instance)
        self.session.add_all(instances)
        self.session.flush()
        self._commit()
        return instances

    def update(self, data: SQLModel | dict) -> Optional[Sequence[T]]:
        """Update tất cả bản ghi khớp filter, trả về số bản ghi được cập nhật."""
        payload = data.model_dump(exclude_none=True) if isinstance(data, SQLModel) else {
            k: v for k, v in data.items() if v is not None
        }
        payload["updated_at"] = datetime.now(UTC)
        stmt = update(self.model)
        if self._filters:
            stmt = stmt.where(*self._filters)
        stmt = stmt.values(**payload).returning(self.model)
        result = self.session.exec(stmt)
        self._commit()
        rows = result.fetchall()
        if not rows:
            return None
        return cast(list[T], [row[0] for row in rows])


    def update_bulk(self, data_list: list[SQLModel] | list[dict]) -> int:
        payload = [
            data.model_dump() if isinstance(data, SQLModel) else data
            for data in data_list
        ]
        self.session.bulk_update_mappings(self.model, payload) # type: ignore
        self.session.commit()
        return len(payload)
    # def update_many(self, data: SQLModel | dict) -> int:
    #     stmt = select(self.model).where(*self._filters)
    #     results = self.session.exec(stmt).all()
    #     data = data.model_dump() if isinstance(data, SQLModel) else data
    #     for obj in results:
    #         for key, value in data.items():
    #             if hasattr(obj, key):
    #                 setattr(obj, key, value)
    #         obj.updated_at = datetime.now(UTC)
    #     self._commit()
    #     return len(results)

    # def update_many(self, data: SQLModel | dict) -> int:
    #     stmt = select(self.model).where(*self._filters)
    #     results = self.session.exec(stmt).all()
    #     data = data.model_dump() if isinstance(data, SQLModel) else data
    #     for obj in results:
    #         for key, value in data.items():
    #             if hasattr(obj, key):
    #                 setattr(obj, key, value)
    #         obj.updated_at = datetime.now(UTC)
    #     self._commit()
    #     return len(results)
    
    def delete(self) -> Optional[T]:
        obj = self.session.exec(select(self.model).where(*self._filters)).first()
        if not obj:
            return None
        self.session.delete(obj)
        self._commit()
        return obj

    # def delete_many(self) -> int:
    #     stmt = delete(self.model).where(*self._filters)
    #     result = self.session.exec(stmt)
    #     self._commit()
    #     return result.rowcount or 0
    # ---- Query ----

    # all()
    def all(self) -> Sequence[T]:
        stmt = select(self.model)

        if self._filters:
            stmt = stmt.where(*self._filters)
        if self._options:
            stmt = stmt.options(*self._options)
        if self._offset:
            stmt = stmt.offset(self._offset)
        if self.limit:
            stmt = stmt.limit(self._limit)
        if self._group_by:
            stmt = stmt.group_by(*self._group_by)
        if self._order_by:
            stmt = stmt.order_by(*self._order_by)
        return self.session.exec(stmt).all()

    # first()
    def first(self) -> Optional[T]:
        stmt = select(self.model)

        if self._filters:
            stmt = stmt.where(*self._filters)
        if self._options:
            stmt = stmt.options(*self._options)
        if self._group_by:
            stmt = stmt.group_by(*self._group_by)
        if self._order_by:
            stmt = stmt.order_by(*self._order_by)
        return self.session.exec(stmt).first()
