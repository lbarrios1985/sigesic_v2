from __future__ import unicode_literals
from django.conf.urls import url, patterns
from unidad_economica.informacion_mercantil.views import MercantilCreate



urlpatterns = [
    url(r'^unidad-economica/sede-administrativa/registro$', 'unidad_economica.informacion_mercantil.views.siguiente', name='siguiente')
]

urlpatterns += [
    url(r'^informacion-mercantil/registro/$', MercantilCreate.as_view(), name='informacion_mercantil'),

]

