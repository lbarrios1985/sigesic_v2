"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.forms
#
# Contiene las clases, atributos y métodos para los formularios a implementar en el módulo de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .constant import (
    TIPO_PERSONA_LIST,
    SHORT_TIPO_PERSONA,
    NACIONALIDAD_LIST,
    FORTALEZA_CONTRASENHA
)
from base.fields import RifField, CedulaField
from base.functions import verificar_rif

import logging

from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, PasswordInput,
    Select
)
from django.contrib.auth.models import User
from django.forms import MultiWidget, Select, TextInput, MultiValueField, ChoiceField, CharField
from django.utils.translation import ugettext_lazy as _

from .constant import SHORT_TIPO_PERSONA

"""!
Contiene el objeto que registra la vitacora de eventos del módulo base.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("base")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class RifForm(forms.Form):
    """!
    Clase que contiene el campo del RIF a incorporar en un formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @version 2.0.0
    """

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()

    def clean_rif(self):
        """!
        Método que permite validar el campo de rif

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el rif no sea válido o no se encuentre registrado en el
                sistema, en caso contrario devuelve el valor actual del campo
        """
        rif = self.cleaned_data['rif']

        if not verificar_rif(rif):
            raise forms.ValidationError(_("El RIF es inválido"))
        elif not User.objects.filter(username=rif):
            raise forms.ValidationError(_("El RIF no esta registrado"))

        return rif


@python_2_unicode_compatible
class ClaveForm(forms.Form):
    """!
    Clase que contiene el campo de contraseña a incorporar en un formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @version 2.0.0
    """

    ## Contraseña del usuario
    clave = CharField(
        label=_("Contraseña"), max_length=30, widget=PasswordInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("contraseña de acceso"), 'data-toggle': 'tooltip',
            'title': _("Indique la contraseña de acceso al sistema"), 'size': '28',
            'onkeyup': 'passwordStrength(this.value)'
        })
    )

    def clean_clave(self):
        """!
        Método que permite validar el campo de contraseña

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la contraseña sea incorrecta, en caso contrario devuelve
                el valor actual del campo
        """
        clave = self.cleaned_data['clave']
        rif = "%s%s%s" % (self.data['rif_0'], self.data['rif_1'], self.data['rif_2'])

        if User.objects.filter(username=rif) and not User.objects.get(username=rif).check_password(clave):
            raise forms.ValidationError(_("Contraseña incorrecta"))

        return clave


@python_2_unicode_compatible
class CaptchaForm(forms.Form):
    """!
    Clase que contiene el campo de captcha a incorporar en un formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @version 2.0.0
    """

    ## Campo de validación de captcha
    captcha = CaptchaField(
        label=_("Captcha"), widget=CaptchaTextInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("texto de la imagen"),
            'style': 'min-width: 0; width: auto; display: inline;', 'data-toggle': 'tooltip',
            'title': _("Indique el texto de la imagen")
        })
    )


@python_2_unicode_compatible
class CorreoForm(forms.Form):
    """!
    Clase que contiene el campo de correo electrónico a incorporar en un formulario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @version 2.0.0
    """

    ## Campo que contiene el correo electrónico
    correo = EmailField(
        label=_("Correo Electrónico"), widget=EmailInput(attrs={
            'class': 'form-control input-sm', 'placeholder': _("Indique su correo"), 'data-toggle': 'tooltip',
            'title': _("Indique el correo electrónico")
        })
    )
