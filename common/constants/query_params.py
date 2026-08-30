class QueryParams:

    def __new__(cls):
        raise TypeError("QueryParams cannot be instantiated.")

    SEARCH = "search"
    PAGE = "page"
    PAGE_SIZE = "page_size"
    ORDERING = "ordering"
    MAX_PAGE_SIZE = 100