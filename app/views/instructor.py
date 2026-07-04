from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from ..models import Instructor , User
from ..serializers import InstructorSerializer , AddInstructorSerializer , CourseSerializer
from ..permissions import Has_role
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

@api_view(['GET','POST'])
@permission_classes([Has_role(User.Role.ADMIN)])
def instructors(request):
    if request.method == 'GET':
        instrctors = Instructor.objects.all()
        serializer = InstructorSerializer(instrctors,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        instructor = AddInstructorSerializer(data=request.data)
        if instructor.is_valid():
            data = instructor.save()
            return Response({"id":data.user.id,
                "username":data.user.username,
                "specialization":data.specialization,
                "experience_years":data.experience_years,
                "phone":data.phone
                })
        return Response(instructor.errors,status=400)

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def instructor(request,id):

    instructor = get_object_or_404(Instructor,id=id)

    if request.method == 'GET':
        if request.user.role not in [User.Role.ADMIN , User.Role.INSTRUCTOR]:
            raise PermissionDenied()
        if request.user.role == User.Role.INSTRUCTOR and request.user.instructor.id != id:
            raise PermissionDenied()
        serailizer = InstructorSerializer(instructor)
        courses = instructor.courses.all()
        ser = CourseSerializer(courses,many=True)
        data = {
            **serailizer.data,
            "courses":ser.data
        }
        return Response(data)
    if request.method == 'PATCH': 
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied()
        serailizer = InstructorSerializer(
            instructor,
            data = request.data,
            partial=True
        )
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        return Response(serailizer.errors,status=400)
        
        







