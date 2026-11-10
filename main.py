from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, model_validator
from typing import Annotated, Optional
import json


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


    
# Creating an instance of FastAPI
app = FastAPI()

def show_json():
    with open('books.json', 'r') as f:
        data = json.load(f)
        return data


def save_Json(data):
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



@app.get("/books")
def show():
    data = show_json()
    return data


# Query Parameter
@app.get("/books/sort")
def sorting(sort_by : str | None = Query(..., description="enter what are you using to sort.", example="title"), desc : bool = False):
    data = show_json()

    sorts = ["title", "year", "pages"]

    if sort_by not in sorts:
        raise HTTPException(status_code=400, detail=f"Invalide sort fill. enter between {sorts}")

    return sorted(data.items(), key=lambda item: item[1][sort_by].lower() if isinstance(item[1][sort_by], str) else item[1][sort_by], reverse=desc)




# Path parameter
@app.get("/books/{book_id}")
def get_book(book_id: str = Path(..., description="for get any perticular book.", example=0)):
    data = show_json()
    if book_id not in data:
        raise HTTPException(status_code=404, detail="Book not found")
    return data[book_id]

@app.post("/creat")
def creat(Book : Book):
    data = show_json()

    existing_titles = [book["title"].casefold() for book in data.values() if "title" in book]

    if Book.book_id in data:
        raise HTTPException(status_code=409, detail="this id is exit in the DB.")

    
    if Book.title.casefold() in existing_titles:
        raise HTTPException(status_code=409, detail="this book is exit in the DB.")
    
    data[Book.book_id] = Book.model_dump(exclude="book_id")

    save_Json(data)

    return JSONResponse(status_code=201, content={"message" : "Book created successfully."})


@app.put("/update/{book_id}")
def update(Update : Update_Book, book_id : str = Path(..., description="give that books id.", example="b001")):
    data = show_json()

    if book_id not in data:
        raise HTTPException(status_code=404, detail="this book id is not exist in the DB.")

    data[book_id].update(Update.model_dump(exclude_unset=True))# we can also use "|=" update operater to do this and looping
    save_Json(data)
    
    return JSONResponse(status_code=201, content={"message" : "Book Updated successfully."})

@app.delete("/remove/{book_id}")
def delete(book_id : str = Path(..., example="b001")):
    data = show_json()

    if book_id not in data:
        raise HTTPException(status_code=404, detail="this book id didn't exist.")

    data.pop(book_id)

    save_Json(data)

    return JSONResponse(status_code=200, content={"message" : "Book deleted successfully."})
