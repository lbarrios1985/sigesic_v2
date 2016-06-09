from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class mimodelo(models.Model):

    """!

    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-06-2016
    @version 2.0.0
    """
    nombre_proceso = models.CharField(max_length=100)

    nombre_maquinaria = models.CharField(max_length=100)

    pais_origen = models.CharField(max_length=100)

    descripcion_maquinaria = models.CharField(max_length=200)

    año_fabricacion = models.IntegerField()

    vida_util = models.IntegerField()

    estado_actual = models.CharField(max_length=50)

    año_adquisicion = models.IntegerField()
