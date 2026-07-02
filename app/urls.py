from django.urls import path
from .views.auth_views import *
from .views.student import *
from .views.instructor import *
urlpatterns = [
    path('getProfile',getProfile),
    path('user',users),
    path('user/<int:id>',user.as_view()),
    path('student',students),
    path('student/<int:id>',student),
    path('instructor',instructors),
    path('instructor/<int:id>',instructor),
]