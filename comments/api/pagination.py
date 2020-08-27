from rest_framework.pagination import (
                                       LimitOffsetPagination, 
                                       PageNumberPagination)


class CommentsPagination(PageNumberPagination):
    page_size = 5