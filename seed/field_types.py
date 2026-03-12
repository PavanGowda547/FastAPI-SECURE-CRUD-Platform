from typing import Annotated
from pydantic import Field

Username = Annotated[str, Field(min_length=3, max_length=20, pattern="^[a-zA-Z0-9_]+$")]
Password = Annotated[str, Field(min_length=8, max_length=100)]
NoteTitle = Annotated[str, Field(min_length=1, max_length=100)]
NoteContent = Annotated[str, Field(max_length=5000)]
