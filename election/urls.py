# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('polling_unit/<int:uniqueid>/', views.polling_unit, name='polling_unit'),
    path('lga/<int:uniqueid>/', views.lga, name='lga'),
]