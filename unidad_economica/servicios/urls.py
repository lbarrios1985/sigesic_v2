from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ServiciosGeneralesCreate

urlpatterns = [
    url(r'^registro', login_required(ServiciosGeneralesCreate.as_view()) ,name="servicio_general_create"),
]