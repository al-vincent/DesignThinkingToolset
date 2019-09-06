from django.urls import path
from PostItFinder import views

app_name = 'PostItFinder'

urlpatterns = [
    path('', views.index, name='index'),
]