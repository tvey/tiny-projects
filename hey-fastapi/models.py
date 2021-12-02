from typing import Optional

from sqlmodel import Field, SQLModel


class Thing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
