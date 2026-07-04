from django.urls import path
from .views.auth_views import *
from .views.student import *
from .views.instructor import *
from .views.course import *
from .views.docs import *
from .views.video import *
urlpatterns = [
    path('getProfile',getProfile),
    path('user',users),
    path('user/<int:id>',user.as_view()),
    path('student',students),
    path('student/<int:id>',student),
    path('instructor',instructors),
    path('instructor/<int:id>',instructor),
    path('course',courses),
    path('course/<int:id>',course),
    path('enroll/<int:course_id>',enroll),
    path('course/<int:course_id>/student/<int:std_id>',course_of_std),
    path('docs',docs),
    path('docs/<int:id>',doc),
    path('videos',videos),
    path('videos/<int:id>',video),
]