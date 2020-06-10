from django.urls import path
from PostItFinder import views

app_name = 'PostItFinder'

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("choose-image/", views.choose_image, name="choose_image"),
    path("set-regions/", views.set_regions, name="set_regions"),
    path("analyse-text/", views.analyse_text, name="analyse_text"),
]