"""Pagination.py."""
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Defines a custom pagination class extends the PageNumberPagination."""

    page_size_query_param = "limit"
