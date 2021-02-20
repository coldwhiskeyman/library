from django.db import models


class Author(models.Model):
    """
    Модель автора
    """
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    birth_year = models.IntegerField('Год рождения')
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    """
    Модель книги
    """
    title = models.CharField('Название', max_length=100)
    isbn = models.IntegerField('ISBN')
    publication_year = models.IntegerField('Год издания')
    sheets_number = models.IntegerField('Количество страниц')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books', verbose_name='Автор')
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = "книга"
        verbose_name_plural = "книги"

    def __str__(self):
        return self.title
