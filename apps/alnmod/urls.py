from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('age/', views.age),
    path('bros/', views.bros),
]