from typing import Optional
from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel,Field
app = FastAPI()

class Book:
    id:int
    title:str
    author:str
    rating:int

    def __init__(self, id,title,author,rating):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating

# Pydantic validation
class BookRequest(BaseModel):
    id:Optional[int] = None
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    rating:int = Field(gt=-1, lt=6)
    # we can add detail information about models what gonna add
    model_config ={}

BOOKS = [
    Book(1,"CS1 Pro","Mert",5),
    Book(2,"CS2 Pro","Mert2",5),
    Book(3,"CS3 Pro","Mert3",4),
    Book(4,"CS4 Pro","Mert4",3),
    Book(5,"CS5 Pro","Mert5",5),
]

@app.get("/bookss")
def read_all_book():
    return BOOKS

# body does not have validation
@app.post("/create-book")
async def create_book(book_request = Body()):
    BOOKS.append(book_request)
    return BOOKS

# Pydantics: which is python library that is used for data modeling,data parsing and efficent error handling
# it is commonly used as resource for data validation and how to handle data coming to our FastApi app
# Create a different request model for data validation
# Field data validation on each variable/element
# We will convert the Pydantics Request into a Book,
# ** operator will pass the key/value from BookRequest() into the Book() constructor
@app.post("/v2/create-book")
async def create_book(book_request: BookRequest):
    # dic removed instead of using dic use model_dump()
    new_book = Book(**book_request.model_dump()) # This code converting request to Book object. 
    BOOKS.append(find_book_id(new_book))
    return BOOKS

def find_book_id(book:Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book
@app.get("/book/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
#order  based on rating
@app.get("/books/sorted")
async def read_book_sorted(order_by:str = Query("rating", description="Sort for title"),
                           order:str =Query("asc", description="Sorting order: asc or desc")
                           ):
    
    sorted_list = sorted(
        BOOKS,
        key=lambda x: getattr(x, order_by),  # Dinamik olarak sıralama yap
        reverse=(order == "desc")  # Eğer "desc" seçildiyse ters çevir
    )
    return sorted_list
        
# Data Validation for Path parameters: we are gonna use Path for validation
@app.get("/v2/book/{book_id}")
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

# Data Valiton for Query Parameters: we are gonna use Query for validation
@app.get("/book-list/")
async def read_book_list(book_rating:int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
 
    return books_to_return