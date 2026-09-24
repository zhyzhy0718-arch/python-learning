from sqlmodel import SQLModel,Field

class NoteBase(SQLModel):
    title: str = Field(index=True)
    content: str | None = None
    category: str | None = Field(default=None, index=True)
    is_archived: bool = False


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_text: str | None = None


class NotePublic(NoteBase):
    id: int


class NoteCreate(NoteBase):
    secret_text: str | None = None


class NoteUpdate(SQLModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    is_archived: bool | None = None
    secret_text: str | None = None