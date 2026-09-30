from common.views.viewsets import BaseModelViewSet
from common.views.api import ProtectedBaseAPiView
from .selectors import CartSelector, CartItemSelector
from common.exceptions.api import NotFoundException
from common.constants.messages import Messages
from common.responses.success import OkResponse, NoContentResponse
from rest_framework.decorators import action
from .serializer import (
    CreateCartSerializer,
    ListCartSerializer,
    DetailCartSerializer
)

class CartViewSet(BaseModelViewSet, ProtectedBaseAPiView):
    
    selector = CartSelector
    
    serializer_action_classes = {
        "create": CreateCartSerializer,
        "list": ListCartSerializer,
        "retrieve": DetailCartSerializer        
    }
    
    @action(
        detail=False,
        methods=["delete"],
        url_path=r"items/(?P<item_id>[^/.]+)",
    )
    def remove_item(self, request, item_id):
        
        cart_item = CartItemSelector.get_or_none(id=item_id)
        
        if not cart_item:
            raise NotFoundException(
                message=Messages.NOT_FOUND
            )

        cart_item.delete()

        return NoContentResponse()
    