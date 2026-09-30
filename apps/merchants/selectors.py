from common.selectors.base import BaseSelector
from .models import Merchant

class MerchantSelector(BaseSelector):
    
    model = Merchant