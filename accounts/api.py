from django.http import JsonResponse
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import User
from .forms import SignupForm
from .serializer import UserSerializer,ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        # Check if the username is unique
        name = form.cleaned_data['name']
        if User.objects.filter(name=name).exists():
            return Response({'message': 'error', 'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email is unique
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return Response({'message': 'error', 'error': 'Email is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        form.save()

        # Send verification email later!
    else:
        message = 'error'

    return Response({'message': message})


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def get_user_data(request, pk):
    try:
        user = User.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            user_avatar = request.FILES.get('user_avatar')

            if user_avatar:
                user.user_avatar = user_avatar
                user.save()
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response({'message': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)       
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Invalid user ID'}, status=400)

    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        if not user.check_password(serializer.validated_data.get("old_password")):
            print("Old password is incorrect")
            return JsonResponse({"old_password": "Wrong password."}, status=400)

        if serializer.validated_data.get("old_password") == serializer.validated_data.get("password"):
            print("New password should be different from the old password.")
            return JsonResponse({"password": "New password should be different from the old password."}, status=400)

        if serializer.validated_data.get("password") != serializer.validated_data.get("password2"):
            print("Passwords do not match.")
            return JsonResponse({"password": "Passwords do not match."}, status=400)

        user.set_password(serializer.validated_data.get("password"))
        user.save()
        return JsonResponse({"message": "Password changed successfully"})
    
    print("Serializer errors:", serializer.errors)
    return JsonResponse(serializer.errors, status=400)

