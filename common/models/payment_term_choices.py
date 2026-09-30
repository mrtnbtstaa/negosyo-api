from django.db import models

class PaymentTermChoices(models.TextChoices):
    CASH = "cash", "Cash"
    COD = "cod", "Cash on Delivery"
    NET_7 = "net 7", "Net 7"
    NET_15 = "net 15", "Net 15"
    NET_30 = "net 30", "Net 30"
    NET_60 = "net 60", "Net 60"