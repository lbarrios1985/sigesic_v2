from django.conf.urls import url
from .views import SucursalCreate

urlpatterns = [
    url(r'^registro', SucursalCreate.as_view() ,name="sucursal_create"),
]