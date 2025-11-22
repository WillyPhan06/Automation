from typing import List
from models.book import Book

def remove_duplicate_books(books: List[Book]) -> List[Book]:
    cleaned_books = []
    seen_titles = set()
    for book in books:
        if book.title not in seen_titles:
            cleaned_books.append(book)
            seen_titles.add(book.title)
    return cleaned_books