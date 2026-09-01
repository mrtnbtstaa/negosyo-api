from rest_framework import serializers
from .models import Customer

class CreateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        read_only_fields = ("id", "user")
        fields = "__all__"


  
