from django.urls import path # type: ignore
from . import views

app_name = 'weather_app'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('weather/', views.weather_details, name='weather_details'),
    path('save_city/', views.save_city, name='save_city'),
    path('saved_cities/', views.saved_cities, name='saved_cities'),
    path('delete_saved_cities/', views.delete_saved_cities_view, name='delete_saved_cities'),
    path('about/', views.about, name='about'),
]
