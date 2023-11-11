from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not username or not password or not first_name or not last_name:
            return Response({"error": "Missing fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "User with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        groups = user.groups.values_list('name', flat=True)

        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'groups': list(groups), 
        }

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        user = User.objects.get(id=request.user.id)

        username = request.data.get('username', user.username)
        first_name = request.data.get('first_name', user.first_name)
        last_name = request.data.get('last_name', user.last_name)
       
        if username != user.username:
            if User.objects.filter(username=username).exists():
                return Response({"error": "User with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        groups = user.groups.values_list('name', flat=True)

        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'groups': list(groups),
        }

        return Response(data, status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = User.objects.get(id=request.user.id)

        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"error": "Missing new password field."}, status=status.HTTP_400_BAD_REQUEST)

        if not current_password or not user.check_password(current_password):
            return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
