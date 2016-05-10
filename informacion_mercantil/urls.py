from django.conf.urls import url
from .views import mercantil

urlpatterns = [
    url(r'^mercantil', mercantil.as_view(), name='mercantil'),
]
