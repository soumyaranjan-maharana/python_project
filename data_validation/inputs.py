from pydantic import BaseModel, Field, computed_field, model_validator
from typing import Annotated, Optional

class Book(BaseModel):
    book_id : Annotated[str, Field(..., examples=["b001"])]
    author : Annotated[str, Field(..., description="write the author name of the book.", examples=["echiro oda", "JKSManga"])]
    country : Annotated[str, Field(default=None, description="write origin of this book if you know.")]
    language : Annotated[str, Field(..., description="enter in which language this  book is writen.", examples=["English", "Hindi"])]
    link : Annotated[str, Field(default=None, description="enter this books link if you have.")]
    pages : Annotated[int, Field(..., description="enter how many pages your book is.")]
    title : Annotated[str, Field(..., description="enter this book title.")]
    year : Annotated[int, Field(..., description="enter this books publish year.")]




    @computed_field
    @property
    def imageLink(self) -> str:
        imageLink = f"images/{self.title}.jpg"
        return imageLink


class Update_Book(BaseModel):
    author : Annotated[Optional[str], Field(default=None, description="write the author name of the book.", examples=["echiro oda", "JKSManga"])]
    country : Annotated[Optional[str], Field(default=None, description="write origin of this book if you know.")]
    language : Annotated[Optional[str], Field(default=None, description="enter in which language this  book is writen.", examples=["English", "Hindi"])]
    link : Annotated[Optional[str], Field(default=None, description="enter this books link if you have.")]
    pages : Annotated[Optional[int], Field(default=None, description="enter how many pages your book is.")]
    year : Annotated[Optional[int], Field(default=None, description="enter this books publish year.")]