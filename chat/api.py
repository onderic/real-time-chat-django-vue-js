from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.serializer import PublicUserSerializer


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def chatPage(request):
#     users = User.objects.exclude(username=request.user.username).values('id', 'username', 'email')
#     print(users)
#     return Response(users)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chatPage(request):
    users = User.objects.exclude(username=request.user.username)
    serializer = PublicUserSerializer(users, many=True)
    data = {
        'users': serializer.data  # Wrap the serialized data in a 'users' key
    }
    return Response(data)
