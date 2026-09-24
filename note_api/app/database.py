from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {
    "check_same_thread": False
}

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args=connect_args
)


def create_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[
    Session,
    Depends(get_session)
]