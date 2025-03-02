from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about.html',views.about,name='about'),
    path('city/<str:city>/', views.city_air_quality, name='city_air_quality'),
    path('city/', views.city_air_quality, name='city_air_quality'),
    path('search_city/', views.search_city, name='search_city'),

]