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
from __future__ import unicode_literals, absolute_import

import logging

from base.constant import (
    TIPO_PERSONA_LIST,
    SHORT_TIPO_PERSONA,
    NACIONALIDAD_LIST,
    FORTALEZA_CONTRASENHA
)
from base.fields import RifField, CedulaField
from base.forms import RifForm, ClaveForm, CaptchaForm, CorreoForm
from base.functions import verificar_rif
from base.classes import Seniat
from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth.models import User
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, PasswordInput,
    Select)
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile

"""!
Contiene el objeto que registra la vitacora de eventos del módulo usuario.
(configuración en el settings de la aplicación)
"""
logger = logging.getLogger("usuario")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


@python_2_unicode_compatible
class AutenticarForm(RifForm, ClaveForm, CaptchaForm):
    """!
    Clase que muestra el formulario de registro de usuarios. Extiende de las clases RifForm, ClaveForm y CaptchaForm

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-04-2016
    @version 2.0.0
    """
    pass

@python_2_unicode_compatible
class OlvidoClaveForm(RifForm, CorreoForm, CaptchaForm):
    """!
    Clase que muestra el formulario para envío de correo electrónico con enlace para la modificación de clave

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 06-05-2016
    @version 2.0.0
    """

    def clean_correo(self):
        correo = self.cleaned_data['correo']

        if not User.objects.filter(email=correo):
            raise forms.ValidationError(_("El correo indicado no existe"))

        return correo


class ModificarClaveForm(ClaveForm, CaptchaForm, forms.Form):

    ## Confirmación de contraseña de acceso
    verificar_contrasenha = CharField(
        label=_("Verificar Contraseña"),
        max_length=128,
        widget=PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Contraseña de acceso"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '50',
                'title': _("Indique nuevamente la contraseña de aceso al sistema")
            }
        )
    )

    def clean_clave(self):
        """!
        Método que permite validar el campo de password

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la fortaleza de la contraseña sea inferior al minimo
                establecido
        """
        password_meter = self.data['passwordMeterId']
        if int(password_meter) < FORTALEZA_CONTRASENHA:
            raise forms.ValidationError(_("La contraseña es débil"))
        return self.cleaned_data['clave']

    def clean_verificar_contrasenha(self):
        """!
        Método que permite validar el campo de verificar_contrasenha

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la contrasenha no pueda ser verificada
        """
        verificar_contrasenha = self.cleaned_data['verificar_contrasenha']
        contrasenha = self.data['clave']
        if contrasenha != verificar_contrasenha:
            raise forms.ValidationError(_("La contraseña no es la misma"))

        return verificar_contrasenha


@python_2_unicode_compatible
class RegistroForm(ModelForm):
    """!
    Clase que muestra el formulario de registro de usuarios

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 21-04-2016
    @version 2.0.0
    """

    ## R.I.F. de la Unidad Económica que identifica al usuario en el sistema
    rif = RifField()

    ## Nombre de la Unidad Economica
    nombre_ue = CharField(
        label=_("Nombre de la Unidad Económica: "),
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Nombre de la Unidad Económica a registrar"), 'readonly': 'readonly', 'size': '50'
            }
        ), required=False
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
                'data-toggle': 'tooltip', 'title': _("Indique el cargo del usuario en la empresa"), 'size': '50'
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
                'data-toggle': 'tooltip', 'title': _("Indique el Nombre"), 'size': '50'
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
                'data-toggle': 'tooltip', 'title': _("Indique el Apellido"), 'size': '50'
            }
        )
    )

    ## Número telefónico de contacto con el usuario
    telefono = CharField(
        label=_("Teléfono"),
        max_length=20,
        widget=TextInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': '(058)-000-0000000',
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '15',
                'title': _("Indique el número telefónico de contacto con el usuario"), 'data-mask': '(000)-000-0000000'
            }
        ),
        help_text=_("(país)-área-número")
    )

    ## Correo electrónico de contacto con el usuario
    correo = EmailField(
        label=_("Correo Electrónico"),
        max_length=75,
        widget=EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'placeholder': _("Correo de contacto"),
                'data-toggle': 'tooltip', 'size': '50', 'data-rule-required': 'true',
                'title': _("Indique el correo electrónico de contacto con el usuario. "
                           "No se permiten correos de hotmail")
            }
        )
    )

    ## Contraseña del usuario
    password = CharField(
        label=_("Contraseña"),
        max_length=128,
        widget=PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'placeholder': _("Contraseña de acceso"),
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '50',
                'title': _("Indique una contraseña de aceso al sistema"), 'onkeyup': 'passwordStrength(this.value)'
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
                'data-rule-required': 'true', 'data-toggle': 'tooltip', 'size': '50',
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
        model = User
        exclude = ['fecha_modpass', 'username', 'first_name', 'last_name', 'email', 'date_joined']


    def clean_rif(self):
        """!
        Método que permite validar el campo de rif

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 27-04-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el rif no sea válido o no se encuentre registrado en el
                SENIAT, en caso contrario devuelve el valor actual del campo
        """
        rif = self.cleaned_data['rif']

        if rif[0] not in TIPO_PERSONA_LIST:
            raise forms.ValidationError(_("Tipo de RIF incorrecto"))
        elif User.objects.filter(username=rif):
            raise forms.ValidationError(_("El RIF ya se encuentra registrado"))
        elif not rif[1:].isdigit():
            raise  forms.ValidationError(_("El RIF no es correcto"))

        return rif

    def clean_cedula(self):
        """!
        Método que permite validar la cedula de identidad del usuario a registrar

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de la cedula de identidad sea incorrecta
        """
        cedula = self.cleaned_data['cedula']

        if cedula[0] not in NACIONALIDAD_LIST:
            raise forms.ValidationError(_("La nacionalidad no es correcta"))
        elif not cedula[1:].isdigit():
            raise forms.ValidationError(_("El número de cédula no es correcto"))

        return cedula

    def clean_correo(self):
        """!
        Método que permite validar el campo de correo electronico

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que el correo electronico ya se encuentre registrado
        """
        correo = self.cleaned_data['correo']

        if User.objects.filter(email=correo):
            raise forms.ValidationError(_("El correo ya esta registrado"))

        return correo

    def clean_password(self):
        """!
        Método que permite validar el campo de password

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la fortaleza de la contraseña sea inferior al minimo
                establecido
        """
        password_meter = self.data['passwordMeterId']
        if int(password_meter) < FORTALEZA_CONTRASENHA:
            raise forms.ValidationError(_("La contraseña es débil"))
        return self.cleaned_data['password']

    def clean_verificar_contrasenha(self):
        """!
        Método que permite validar el campo de verificar_contrasenha

        @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 02-05-2016
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve un mensaje de error en caso de que la contrasenha no pueda ser verificada
        """
        verificar_contrasenha = self.cleaned_data['verificar_contrasenha']
        contrasenha = self.data['password']
        if contrasenha != verificar_contrasenha:
            raise forms.ValidationError(_("La contraseña no es la misma"))

        return verificar_contrasenha


class PerfilForm(RegistroForm):
    """!
    Clase que muestra el formulario del perfil del usuario

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 07-05-2016
    @version 2.0.0
    """

    class Meta:
        model = User
        exclude = ['fecha_modpass', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'username', 'rif']