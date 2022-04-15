from rest_framework import serializers
from .models import Account
 
# create a serializer class
class AccountSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Account
        fields = ('username', 'password',)