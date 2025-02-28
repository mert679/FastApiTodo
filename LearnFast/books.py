from fastapi import FastAPI, Body

app = FastAPI()

# we do not need to add every function async because FastAPi add async behind the scenes.
# we can run server with two section: first uvicorn books:app --reload --port 8002
# other way to do it fastapi run books.py --port 8002, the third way fastapi dev books.py


# {} içinde dict kullanamazsınız çünkü dict değiştirilebilir bir veri tipidir.
BOOKS = [
    {"title":"Geceler1", "author":"Author1", "category":"science1"},
    {"title":"Geceler2", "author":"Author2", "category":"science2"},
    {"title":"Geceler3", "author":"Author3", "category":"science34"},
    {"title":"Geceler4", "author":"Author4", "category":"science4"},
    {"title":"Geceler5", "author":"Author5", "category":"science5"},
]
@app.get("/bookss")
def read_all_book():
    return BOOKS

# Path Parameters: request parameters that have been attached to the URL
@app.get("/book/{title}")
async def book_detail(title:str):
    
    for book in BOOKS:
        #casefold is caseless comparisan function
        if book.get("title").casefold() == title.casefold():
            return book

#Query Parameters: request parameters that have been attached after a ? have name=value pairs we gonna search and filter with query paramaters

@app.get("/books")
async def book_list(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}")
async def read_category(book_author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold() and book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#Get cannot have a body. Post have it.
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

#Put: used to update data. put also have body.
@app.patch("/books/{title}/update")
async def update_book(title:str, updated_book = Body()):
    for book in BOOKS:
        if book.get("title").casefold() == title.casefold():
            book.update(updated_book)

    return BOOKS

#Delete: To delete fonksion it
@app.delete("/books/{title}/delete")
async def delete_book(title:str):
    global BOOKS  # Listeyi değiştirmek için global yapıyoruz
    for book in BOOKS:
        if book.get("title").casefold() == title.casefold():
            BOOKS.remove(book)

    return BOOKS