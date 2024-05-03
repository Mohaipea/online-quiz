from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<str:pk>', views.quiz, name='quiz'),
    path('question/<str:pk>', views.question, name='question'),
    path('answer/<str:pk>/<str:name>', views.answer, name='answer'),
    path('finish/<str:pk>', views.finish, name='finish'),
    path('create-quiz/', views.createQuiz, name='create_quiz'),
    path('create-question/<str:pk>', views.createQuestion, name='create_question'),
    path('create-answer/<str:pk>', views.createAnswer, name='create_answer')
]