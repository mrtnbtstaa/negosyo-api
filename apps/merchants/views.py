from common.views.viewsets import BaseModelViewSet
from common.views.api import ProtectedBaseAPiView
from common.responses.success import CreatedResponse
from common.constants.messages import Messages
from rest_framework import generics
from .services import MerchantService
from rest_framework.decorators import action
from .selectors import MerchantSelector
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from apps.product_stock.serializers import ProductStockSerializer
from .serializers import (
    CreateMerchantSerializer,
    RegisterMerchantAccountSerializer,
    ListMerchantSerializer,
    DetailMerchantSerializer
)

class MerchantViewSet(BaseModelViewSet, ProtectedBaseAPiView):
    
    selector = MerchantSelector
    
    serializer_action_classes = {
        "create": CreateMerchantSerializer,
        "list": ListMerchantSerializer,
        "retrieve": DetailMerchantSerializer,
        "register": RegisterMerchantAccountSerializer
    }
    
    def get_object(self):
        
        if self.action == "retrieve":
            slug = self.kwargs.get("pk")  
            return get_object_or_404(
                self.get_queryset(),
                slug=slug
            )
        return super().get_object()
    
    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def register(self, request, pk=None):
        
        serializer = RegisterMerchantAccountSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
                    
        MerchantService.register_merchant_account(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        
        return CreatedResponse(
            message=Messages.CREATED
        )
        
    @action(detail=True, methods=["GET"], url_path="products")
    def products(self, request, pk=None):
        
        merchant = self.get_object()
        
        queryset = merchant.product_stocks.prefetch_related('merchant').all()
        
        page = self.paginate_queryset(queryset)
        
        serializer = ProductStockSerializer(
            page,
            many=True,
            context=self.get_serializer_context()
        )
        
        print(serializer.data)
        
        return self.get_paginated_response(serializer.data)
           
class UpdateMerchantView(ProtectedBaseAPiView, generics.UpdateAPIView):
       
    def patch(self, request):
        MerchantService.complete_business_owner_onboarding(
            user=request.user
        )
        
        return CreatedResponse(
            message=Messages.UPDATED
        )