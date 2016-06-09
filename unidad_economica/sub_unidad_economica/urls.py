from django.conf.urls import url
from .views import SubUnidadEconomicaCreate, SubUnidadFormAjax

urlpatterns = [
    url(r'^registro', SubUnidadEconomicaCreate.as_view() ,name="sub_unidad_create"),
    url(r'^form-ajax', SubUnidadFormAjax.as_view() ,name="sub_unidad_ajax"),
]