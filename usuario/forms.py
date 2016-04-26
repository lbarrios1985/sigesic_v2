"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace usuario.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals
from django import forms
from django.forms import (
    ModelForm, ChoiceField, TextInput, EmailInput, CharField, Select, EmailField, ModelChoiceField, PasswordInput,
    HiddenInput
)
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField, CaptchaTextInput
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.constant import (
    NACIONALIDAD, TIPO_PERSONA, SHORT_TIPO_PERSONA
)

from base.fields import RifField, CedulaField
from .models import UserProfile

import logging

"""!
Contiene el objeto que registra la vitacora de eventos del módulo usuario.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("usuario")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class AutenticarForm(forms.Form):
    """!
    Clase que muestra el formulario de registro de usuarios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-04-2016
    @version 2.0.0
    """

    ## Tipo de persona que identifica al número del R.I.F.
    tipo_rif = ChoiceField(
        label=_("R.I.F. de la Unidad Economica"),
        choices=SHORT_TIPO_PERSONA,
        widget=Select(
            attrs={
                'class': 'select2 form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione el tipo de R.I.F.")
            }
        )
    )

    ## Número de R.I.F. de 8 dígitos
    numero_rif = CharField(
        label='',
        max_length=8,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Nro. de R.I.F."), 'data-rule-required': 'true',
                'data-toggle': 'tooltip',
                'title': _("Indique el número de R.I.F., si es menor a 8 dígitos complete con ceros a la izquierda")
            }
        )
    )

    ## Dígito validador del R.I.F.
    digito_validador_rif = CharField(
        label='',
        max_length=1,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Indique el último dígito del R.I.F."), 'placeholder': 'X'
            }
        )
    )

    ## Contraseña del usuario
    clave = CharField(
        label=_("Contraseña"), max_length=30, widget=PasswordInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("contraseña de acceso"), 'data-toggle': 'tooltip',
            'title': _("Indique la contraseña de acceso al sistema")
        })
    )

    ## Campo de validación de captcha
    captcha = CaptchaField(
        label=_("Captcha"), widget=CaptchaTextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("texto de la imagen"),
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique el texto de la imagen")
        })
    )


@python_2_unicode_compatible
class RegistroForm(ModelForm):
    """!
    Clase que muestra el formulario de registro de usuarios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-04-2016
    @version 2.0.0
    """

    ## Tipo de persona que identifica al número del R.I.F.
    """tipo_rif = ChoiceField(
        label=_("R.I.F. de la Unidad Economica"),
        choices=SHORT_TIPO_PERSONA,
        widget=Select(
            attrs={
                'class': 'select2 select2-offscreen form-control', 'data-toggle': 'tooltip',
                'title': _("Seleccione el tipo de R.I.F.")
            }
        )
    )

    ## Número de R.I.F. de 8 dígitos
    numero_rif = CharField(
        label='',
        max_length=8,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Nro. de R.I.F."), 'data-rule-required': 'true',
                'data-toggle': 'tooltip',
                'title': _("Indique el número de R.I.F., si es menor a 8 dígitos complete con ceros a la izquierda")
            }
        )
    )

    ## Dígito validador del R.I.F.
    digito_validador_rif = CharField(
        label='',
        max_length=1,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Indique el último dígito del R.I.F.")
            }
        )
    )"""
    rif = RifField()

    ## Nombre de la Unidad Economica
    nombre_ue = CharField(
        label=_("Nombre de la Unidad Económica: "),
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Nombre de la Unidad Económica a registrar"), 'readonly': 'readonly'
            }
        )
    )

    ## Cédula de Identidad del usuario
    cedula = CedulaField()

    ## Cargo del usuario dentro de la Unidad Económica
    cargo = CharField(
        label=_("Cargo que ocupa en la U.E.:"),
        max_length=175,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Cargo en la Empresa"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el cargo del usuario en la empresa")
            }
        )
    )

    ## Nombre del usuario
    nombre = CharField(
        label=_("Nombre"),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Nombres del usuario"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Nombre")
            }
        )
    )

    ## Apellido del usuario
    apellido = CharField(
        label=_("Apellido"),
        max_length=30,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Apellidos del usuario"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el Apellido")
            }
        )
    )

    ## Número telefónico de contacto con el usuario
    telefono = CharField(
        label=_("Teléfono"),
        max_length=15,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Número telefónico"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip', 'title': _("Indique el número telefónico de contacto con el usuario")
            }
        )
    )

    ## Correo electrónico de contacto con el usuario
    correo = EmailField(
        label=_("Correo Electrónico"),
        max_length=15,
        widget=EmailInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Correo de contacto"), 'data-rule-required': 'true',
                'data-toggle': 'tooltip',
                'title': _("Indique el correo electrónico de contacto con el usuario. "
                           "No se permiten correos de hotmail")
            }
        )
    )

    ## Contraseña del usuario
    contrasenha = CharField(
        label=_("Contraseña"),
        max_length=128,
        widget=PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Contraseña de acceso"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Indique una contraseña de aceso al sistema")
            }
        )
    )

    ## Confirmación de contraseña de acceso
    verificar_contrasenha = CharField(
        label=_("Verificar Contraseña"),
        max_length=128,
        widget=PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Contraseña de acceso"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Indique nuevamente la contraseña de aceso al sistema")
            }
        )
    )

    ## Campo para la validación del captcha
    captcha = CaptchaField(
        label=_(u"Captcha"), widget=CaptchaTextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Texto de la imagen"),
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _(u"Indique el texto de la imagen")
        })
    )

    class Meta:
        model = UserProfile
        exclude = ['fecha_modpass',]


    def clean_nacionalidad(self):
        pass

    def clean_cedula(self):
        pass

    def clean_cargo(self):
        pass

    def clean_nombre(self):
        pass

    def clean_apellido(self):
        pass

    def clean_correo(self):
        pass

    def clean_telefono(self):
        pass

    def clean_contrasenha(self):
        pass

    def clean_verificar_contrasenha(self):
        pass

    def clean_captcha(self):
        pass