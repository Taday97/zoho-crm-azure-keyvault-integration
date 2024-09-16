from django.db.models import fields
from rest_framework import serializers
from server.models import Lead    
class LeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lead  
        fields='__all__'