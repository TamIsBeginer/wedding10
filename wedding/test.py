from .serializers import UserSerializer
from .models import *

print(UserSerializer(User.objects.all(), many=True).data)