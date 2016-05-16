from django.conf.urls import url
from .views import UnidadComercializadoraCreate

urlpatterns = [
    url(r'^registro', UnidadComercializadoraCreate.as_view() ,name="unidades_comercializadoras_create"),
]