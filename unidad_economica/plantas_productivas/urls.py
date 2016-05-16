from django.conf.urls import url
from .views import PlantasProductivasCreate

urlpatterns = [
    url(r'^registro', PlantasProductivasCreate.as_view() ,name="plantas_create"),
]