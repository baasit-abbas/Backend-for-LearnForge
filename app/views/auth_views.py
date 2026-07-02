from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view , APIView , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..permissions import Has_role
from ..models import User
from ..serializers import UserSerializer
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    return Response({
        "id":request.user.id,
        "username":request.user.username,
        "email":request.user.email,
        "role":request.user.role
        })

@api_view(['GET'])
@permission_classes([Has_role(User.Role.ADMIN)])
def users(request):
    user = User.objects.all()
    serializer = UserSerializer(user,many=True)
    return Response(serializer.data)

class user(APIView):
    permission_classes = [Has_role(User.Role.ADMIN)]

    def get(self,request,id):
        user = get_object_or_404(User,id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def patch(self,request,id):
        user = get_object_or_404(User,id=id)
        serializer = UserSerializer(
            user,
            data = request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,id):
        user = get_object_or_404(User,id=id)
        user.delete()
        return Response({
            "message":"User deleted","status":200
        })
    







