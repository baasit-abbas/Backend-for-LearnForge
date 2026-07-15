from django.urls import path
from .views.auth_views import *
from .views.student import *
from .views.instructor import *
from .views.course import *
from .views.docs import *
from .views.video import *
from .views.quiz import *
from .views.tutor import *
from .views.flashcard import *

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
    path('docs',docs),
    path('docs/<int:id>',doc),
    path('videos',videos),
    path('videos/<int:id>',video),
    path('quiz',quizes),
    path('quiz/<int:id>',quiz),
    path('quiz/<int:quiz_id>/selected/<int:selected_id>',selected),
    path('chat',chats),
    path('chat/<int:id>',chat),
    path('flashcards',flashcards),
    path('flashcards/course/<int:id>',flashcard)
]