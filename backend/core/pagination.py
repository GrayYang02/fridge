from rest_framework.pagination import PageNumberPagination


# Custom Pagination Class
class UserRecipeLogPagination(PageNumberPagination):
    page_size = 5  # Default number of items per page
    page_size_query_param = "page_size"  # Allow client to specify custom page size
    max_page_size = 10  # Prevent excessive queries

