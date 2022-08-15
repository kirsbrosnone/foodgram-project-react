from rest_framework.pagination import PageNumberPagination


class MainPagination(PageNumberPagination):
    """Кастомный класс пагинации с поддержкой параметра limit."""

    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 12
