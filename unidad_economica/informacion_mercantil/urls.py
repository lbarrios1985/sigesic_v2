from django.conf.urls import url
from .views import MercantilCreate

urlpatterns = [
    url(r'^informacion-mercantil/registro/$', MercantilCreate.as_view(), name='informacion_mercantil'),
]
