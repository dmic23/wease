import json
from django.utils import timezone
from datetime import date
from swampdragon.serializers.model_serializer import ModelSerializer
from authentication.models import Account, Company

class UserSerializer(ModelSerializer):
    
    def serialize_user_name_full(self, obj):
        return ' '.join([obj.first_name, obj.last_name])

    def serialize_user_pic(self, obj):
        return unicode(obj.user_pic)
        
    class Meta:
        model = Account
        publish_fields = ('id', 'email', 'username', 'user_name_full', 'first_name', 'last_name', 'optiz', 'lang', 
                'user_company', 'position', 'access_level', 'auth_amount', 'street_addr1',
                'street_addr2', 'city', 'post_code', 'country', 'phone_main', 'phone_mobile', 'user_pic',)
