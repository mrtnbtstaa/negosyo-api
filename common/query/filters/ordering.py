from rest_framework.filters import OrderingFilter

class SelectorOrderingFilter(OrderingFilter):  

    def get_default_ordering(self, view):

        selector = getattr(view, "selector", None)

        if selector is None:
            return None

        return selector.default_ordering
