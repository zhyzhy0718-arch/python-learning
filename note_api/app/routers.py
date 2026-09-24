from .database import SessionDep
from fastapi import HTTPException
from fastapi import APIRouter,Query
from .models import Note, NoteCreate, NotePublic, NoteUpdate
from sqlmodel import select
router = APIRouter(prefix="/notes",
                   tags=["notes"],
)

@router.post(
    "/",
    response_model=NotePublic,
    status_code=201
)
def create_note(note: NoteCreate, session: SessionDep):
    note_db = Note.model_validate(note)

    session.add(note_db)
    session.commit()
    session.refresh(note_db)

    return note_db


@router.get(
    "/{note_id}",
    response_model=NotePublic
)
def get_note(note_id: int, session: SessionDep):
    note_db = session.get(Note, note_id)
    if not note_db:
        raise HTTPException(status_code=404, detail="Note not found")

    return note_db


@router.get(
    "/",
    response_model=list[NotePublic]
)
def read_notes(session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    category: str | None = None,
    is_archived: bool | None = None
):
    statement = select(Note)

    if category is not None:
        statement = statement.where(
            Note.category == category
        )

    if is_archived is not None:
        statement = statement.where(
            Note.is_archived == is_archived
        )

    statement = statement.offset(offset).limit(limit)

    notes = session.exec(statement).all()

    return notes


@router.patch(
    "/{note_id}",
    response_model=NotePublic
)
def update_note(
    note_id: int,
    note: NoteUpdate,
    session: SessionDep
):
    note_db = session.get(Note, note_id)
    if not note_db:
        raise HTTPException(status_code=404, detail="Note not found")
    note_data = note.model_dump(
        exclude_unset=True
    )

    note_db.sqlmodel_update(note_data)

    session.commit()
    session.refresh(note_db)

    return note_db


@router.delete("/{note_id}")
def delete_note(note_id: int, session: SessionDep):
    note_db = session.get(Note, note_id)
    if not note_db:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note_db)
    session.commit()

    return {"ok": True}