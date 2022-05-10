from rest_framework import pagination


class BasePaginator(pagination.PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
