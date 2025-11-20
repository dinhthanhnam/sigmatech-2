from models.base import Base
from sqlmodel import SQLModel, Session, create_engine, MetaData, text
import pytest
from typing import Optional, cast
from db import clear_session, test_engine, get_session
from utils.crypto import hash, verify_password

def test_hash_verify_password():
    plain = '123443534'
    hashed = hash(plain)
    assert verify_password(plain, hashed)