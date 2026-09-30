from common.selectors.base import BaseSelector
from .models import ProductStock

class ProductStockSelector(BaseSelector):
    
    model = ProductStock
    
    searchable_fields = ("product_name", "category", "stock_status")
    
    filterable_fields = {
        "category": ("exact", ),
        "stock_status": ("exact", )
    }