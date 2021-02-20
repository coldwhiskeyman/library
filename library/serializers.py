from rest_framework import serializers

from library.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели автора
    """
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'birth_year']


class BookSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели книги
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_year', 'sheets_number']
