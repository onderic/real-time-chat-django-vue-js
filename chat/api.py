from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chatPage(request):
    users = User.objects.exclude(username=request.user.username)
    context = {'users': users}
    return Response(context)