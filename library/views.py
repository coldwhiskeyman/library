from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from library.models import Author, Book
from library.serializers import AuthorSerializer, BookSerializer


class ActiveRecordsOnlyMixin:
    """
    Миксин, позволяющий установить доступ только к записям
    с флагом is_active = True
    """
    def get_queryset(self):
        if self.action == 'set_active':
            return super(ActiveRecordsOnlyMixin, self).get_queryset()
        return super(ActiveRecordsOnlyMixin, self).get_queryset().filter(is_active=True)

    @action(detail=True, methods=['post'])
    def set_active(self, request, pk):
        """
        Метод для управления флагом is_active.
        Доступен администраторам.
        :param request: объект запроса
        :param pk: id записи БД
        """
        if request.user.is_staff:
            obj = self.get_object()
            value = request.POST['value']
            if value == 'true':
                obj.is_active = True
                obj.save()
            elif value == 'false':
                obj.is_active = False
                obj.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AuthorViewSet(ActiveRecordsOnlyMixin, viewsets.ModelViewSet):
    """
    API модели автора
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_filtered_queryset(self, queryset):
        """
        Фильтрация результата по аргументам запроса
        """
        name = self.request.query_params.get('name')

        if name:
            name_split = name.title().split()
            if len(name_split) == 2:
                queryset = queryset.filter(first_name=name_split[0], last_name=name_split[1])
            else:
                queryset = queryset.filter(last_name=name_split[0])
        return queryset

    def get_queryset(self):
        queryset = super(AuthorViewSet, self).get_queryset()
        queryset = self.get_filtered_queryset(queryset)
        return queryset


class BookViewSet(ActiveRecordsOnlyMixin, viewsets.ModelViewSet):
    """
    API модели книг
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_filtered_queryset(self, queryset):
        """
        Фильтрация результата по аргументам запроса
        """
        author = self.request.query_params.get('author')
        title = self.request.query_params.get('title')
        pages = self.request.query_params.get('pages')
        operator = self.request.query_params.get('operator')
        filters = {}

        if author:
            author_id = Author.objects.get(last_name=author).id
            filters['author'] = author_id
        if title:
            filters['title'] = title
        if pages:
            if not operator:
                filters['sheets_number'] = pages
            else:
                if operator == 'gt':
                    filters['sheets_number__gt'] = pages
                elif operator == 'lt':
                    filters['sheets_number__lt'] = pages
        return queryset.filter(**filters)

    def get_queryset(self):
        queryset = super(BookViewSet, self).get_queryset()
        queryset = self.get_filtered_queryset(queryset)
        return queryset
