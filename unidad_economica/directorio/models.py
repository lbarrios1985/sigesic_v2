"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace unidad_economica.directorio.models
#
# Contiene las clases, atributos y métodos para el modelo de datos del directorio
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DirectorioModel(models.Model):
    """!
    Clase que gestiona los datos del directorio

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 05-05-2016
    @version 2.0.0
    """
    
    ## Va a contener los prefijos Autopista, Avenida, Carretera, Calle, Carrera, Vereda 
    prefijo1 = models.CharField(max_length=20)
    
    ## Va a contener la descripción de la dirección en el primer prefijo
    nombre1 = models.CharField(max_length=20)
    
    ## Va a contener los prefijos Edificio, Galpón, Centro Comercial, Quinta, Casa, Local 
    prefijo2 = models.CharField(max_length=20)
    
    ## Va a contener la descripción de la dirección en el segundo prefijo
    nombre2 = models.CharField(max_length=20)
    
    ## Va a contener los prefijos Local, Oficina, Apartamento 
    prefijo3 = models.CharField(max_length=20)
    
    ## Va a contener la descripción de la dirección en el tercer prefijo
    nombre3 = models.CharField(max_length=20)
    
    ## Va a contener los prefijos Urbanización, Sector, Zona 
    prefijo4 = models.CharField(max_length=20)
    
    ## Va a contener la descripción de la dirección en el cuarto prefijo
    nombre4 = models.CharField(max_length=20)
    
    ## Muestra si la dirección esta activa o no
    activo = models.BooleanField()
    
    ## Contiene la relación con el modelo User de django
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    
    ## Contiene la relación con el modelos Parroquia
    #parroquia_id = models.OneToOneField()