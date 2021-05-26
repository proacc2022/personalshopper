from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/', views.home, name='chatbot_home'),
    path('get/', views.get_response, name='get_response'),
]
