from django.urls import path,include
from . import views

urlpatterns = [
 path('recommendations/', views.recommendations, name='recommendations'),
]