from django.conf.urls import url
from .views import SubUnidadEconomicaCreate, SubUnidadFormProcesoAjax, SubUnidadFormActividadAjax

urlpatterns = [
    url(r'^registro', SubUnidadEconomicaCreate.as_view() ,name="sub_unidad_create"),
    url(r'^form-proceso-ajax', SubUnidadFormProcesoAjax.as_view() ,name="sub_unidad_proceso_ajax"),
    url(r'^form-actividad-ajax', SubUnidadFormActividadAjax.as_view() ,name="sub_unidad_actividad_ajax"),
]