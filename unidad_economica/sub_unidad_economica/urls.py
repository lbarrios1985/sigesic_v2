from django.conf.urls import url
from .views import PlantasCreate

urlpatterns = [
    url(r'^plantas_productivas', PlantasCreate.as_view() ,name="plantas_productivas_form"),
]