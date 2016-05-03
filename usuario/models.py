"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace usuario.models
#
# Contiene las clases, atributos y métodos para el modelo de datos de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.constant import NACIONALIDAD

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class UserProfile(models.Model):
    """!
    Clase que gestiona los datos de los usuarios que tendrán acceso al sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-04-2016
    @version 2.0.0
    """

    ## Establece la nacionalidad del usuario
    nacionalidad = models.CharField(
        max_length=1, choices=NACIONALIDAD, help_text=_("Nacionalidad del usuario")
    )

    ## Establece la cédula de identidad del usuario
    cedula = models.CharField(
        max_length=8, help_text=_("Cédula de Identidad del usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d]{7,8}+$',
                _("Introduzca un número de cédula válido. Solo se permiten números y una longitud de 7 u 8 carácteres.")
            ),
        ]
    )

    ## Establece el cargo del usuario dentro de la unidad económica
    cargo = models.CharField(
        max_length=175, help_text=_("Cargo del usuario dentro de la Unidad Económica")
    )

    ## Establece el teléfono de contacto del usuario
    telefono = models.CharField(
        max_length=20, help_text=_("Número telefónico de contacto con el usuario"),
        validators=[
            validators.RegexValidator(
                r'^[\d+-]+$',
                _("Número telefónico inválido. Solo se permiten números, y los signos + o -")
            ),
        ]
    )

    ## Establece la última fecha de modificación de la contraseña, lo cual permite establecer la caducidad de la misma
    fecha_modpass = models.DateTimeField(null=True, help_text=_("Fecha en la que se modificó la contraseña"))

    ## Establece la relación entre el usuario y el perfil
    user = models.OneToOneField(
        User, related_name="profile",
        help_text=_("Relación entre los datos de registro de la unidad económica y el usuario con acceso al sistema")
    )

    class Meta:
        """!
        Metaclase que permite establecer las propiedades de la clase UserProfile

        @author Ing. Roldan Vargas rvargas at cenditel.gob.ve
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 20-04-2016
        @version 2.0.0
        """
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")
        ordering = ("cedula",)

    def __str__(self):
        """!
        Método que muestra la información sobre el perfil del usuario

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 20-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve los datos del perfil del usuario
        """
        return "%s, %s" % (six.text_type(self.user.first_name), six.text_type(self.user.last_name))