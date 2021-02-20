from django.contrib import admin

from library.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Регистрация модели автора в админ-интерфейсе
    """
    list_display = ['first_name', 'last_name', 'birth_year']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Регистрация модели книги в админ-интерфейсе
    """
    list_display = ['title', 'author', 'isbn', 'publication_year', 'sheets_number']
