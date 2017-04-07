"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace base.constant
#
# Contiene constantes de uso general en la aplicación
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"


## Estatus de las notificaciones
ESTATUS_NOTIFICACION = (
    ("N", _("Notificado")),
    ("L", _("Leído")),
    ("P", _("Registrando")),
    ("C", _("Culminado")),
)

## Estatus por defecto de las notificaciones
ESTATUS_NOTIFICACION_DEFAULT = 'N'

## Nacionalidades
NACIONALIDAD = (
    ("V", _("Venezolano")),
    ("E", _("Extranjero"))
)

##Naturaleza Juridica
NATURALEZA_JURIDICA = [
    ("S.A", _("Sociedad Anónima")),
    ("C.A", _("Compañía Anónima")),
    ("S.R.L.", _("Sociedad de Responsabilidad Limitada")),
    ("Co", _("Cooperativa")),
    ("F.P.", _("Firma Personal")),
    ("F.P.A.B.", _("Firma Personal Asociada a la Banca")),
    ("S.A.C.A.", _("Sociedad Anónima de Capital Autorizado")),
]

##Cargo del Representante Legal
CARGO_REP = [
    ("Accionista", _("Accionista")),
    ("Director", _("Director")),
    ("Consultor Jurídico", _("Consultor Jurídico")),
    ("Presidente", _("Presidente")),
    ("Vicepresidente", _("Vicepresidente")),
    ("Otro", _("Otro"))
]

## TIPOS DE PERSONALIDAD
TIPO_PERSONA = (
    ("V", _("Natural")),
    ("J", _("Jurídica")),
    ("E", _("Extranjera")),
    ("P", _("Pasaporte"))
)

## TIPOS DE PERSONALIDAD (ABREVIADO)
SHORT_TIPO_PERSONA = (
    ("V", "V"), ("J", "J"), ("E", "E"), ("P", "P")
)

## Lista de tipos de persona
TIPO_PERSONA_LIST = [tp[0] for tp in SHORT_TIPO_PERSONA]

## Nacionalidades (ABREVIADO)
SHORT_NACIONALIDAD = (
    ("V", "V"), ("E", "E")
)

## Lista de nacionalidades
NACIONALIDAD_LIST = [nac[0] for nac in SHORT_NACIONALIDAD]

## Turno de atención al público
TURNO = (
    ("M", _("Mañana")),
    ("T", _("Tarde"))
)

## Respuesta de selección
SELECCION = (
  ("N", _("NO")),
  ("S", _("SI"))
)

## Prefijos permitidos para el primer campo de direcciones
PREFIJO_DIRECTORIO_UNO_CHOICES = (
    ('AU', _("Autopista")),
    ('AV', _("Avenida")),
    ('CA', _("Carretera")),
    ('CL', _("Calle")),
    ('CR', _("Carrera")),
    ('VR', _("Vereda")),
)

## Prefijos permitidos para el segundo campo de direcciones
PREFIJO_DIRECTORIO_DOS_CHOICES = (
    ('ED', _("Edificio")),
    ('GA', _("Galpón")),
    ('QT', _("Quinta")),
    ('CA', _("Casa")),
    ('CC', _("Centro Comercial")),
)

## Prefijos permitidos para el tercer campo de direcciones
PREFIJO_DIRECTORIO_TRES_CHOICES = (
    ('LC', _("Local")),
    ('OF', _("Oficina")),
    ('AP', _("Apartamento")),
)

## Prefijos permitidos para el cuarto campo de direcciones
PREFIJO_DIRECTORIO_CUATRO_CHOICES = (
    ('UB', _("Urbanización")),
    ('SC', _("Sector")),
    ('ZR', _("Zona Residencial")),
    ('ZI', _("Zona Industrial")),
)

## Tipos de Sub-Unidad Económica
TIPO_SUB_UNIDAD = (
    ('Se', _("Sede Administrativa")),
    ('Pl', _("Planta Productiva")),
    ('Su', _("Sucursal")),
)

## PERIODO DE VERIFICACION DE LA CADUCIDAD DE LA CONTRASEÑA EN DIAS
ACTUALIZACION_PASSWORD = 90

## Nombre del Sitio
APP_NAME = "SIGESIC"

## Asunto del mensaje de bienvenida
EMAIL_SUBJECT_REGISTRO = "Bienvenido a %s" % APP_NAME

## Asunto en el procesamiento de archivos de carga masiva
EMAIL_SUBJECT_CM_RESULT = "Resultado en registro de datos de %s"

admin_email = ''
if settings.ADMINS:
    ## Contiene el correo electrónico del administrador del sistema
    admin_email = settings.ADMINS[0][1]

## Mensaje de bienvenida utilizado en el registro de usuarios
REGISTRO_MESSAGE = '%s %s %s (spam) %s %s' % \
                   (str(_("Hemos enviado un mensaje de bienvenida con un enlace de activación a la dirección de correo "
                          "suministrada.")),
                    str(_("Por favor confirme el registro haciendo click en el enlace enviado por correo (si lo "
                          "prefiere también puede copiar y pegar el enlace en su navegador).")),
                    str(_("En caso de no recibir el correo enviado por el sistema en su bandeja de entrada, "
                          "se le recomienda revisar la carpeta de correos no deseados")),
                    str(_("y verificar si existe, en caso afirmativo le recomendamos agregar la dirección de correo de "
                          "la aplicación en la libreta de direcciones de su cuenta de correo para que en futuras "
                          "ocasiones no sea filtrado. En caso contrario contacte al administrador del sistema")),
                    str(admin_email))

## Mensaje a mostrar al usuario cuando el registro de datos haya sido ejecutado correctamente
CREATE_MESSAGE = _("Los datos fueron registrados correctamente")

## Mensaje a mostrar cuando los datos hayan sido actualizados correctamente
UPDATE_MESSAGE = _("Los datos fueron actualizados correctamente")

## Mensaje a mostrar cuando los datos hayan sido eliminados correctamente
DELETE_MESSAGE = _("El registro seleccionado fue eliminado correctamente")

## Mensaje a mostrar cuando el usuario solicita una nueva contraseña
NUEVA_CLAVE_MESSAGE = _("¡La nueva contraseña fue enviada a su dirección de correo electrónico!")

## Mensaje desautenticación en el sistema
LOGOUT_SECURITY_MESSAGE = _("Por su seguridad usted a sido desautenticado del sistema, debe ingresar nuevamente.")

## Mensaje de error para peticiones AJAX
MSG_NOT_AJAX = _("No se puede procesar la petición. "
                 "Verifique que posea las opciones javascript habilitadas e intente nuevamente.")

## Mensaje de error al descargar archivos
MSG_NOT_DOWNLOAD_FILE = _("No ha proporcionado los datos para la descarga del archivo. Verifique!!!")

## Mensaje de error al cargar archivos
MSG_NOT_UPLOAD_FILE = _("No ha proporcionado los datos para cargar la información. Verifique!!!")

## Mensaje que indica si existen errores en la carga de datos
MSG_SAVE_DATA_CM = _("Se encontraron errores al procesar el archivo, será notificado por correo electrónico con los detalles.")

## Determina el nivel mínimo de validación para la fortaleza de la contraseña. Los valores permitidos son del 0 al 5
FORTALEZA_CONTRASENHA = 3

## Días de caducidad para el enlace de registro de usuarios
CADUCIDAD_LINK_REGISTRO = 1

## Estado Actual de la maquinaria o el equipo
ESTADO_ACTUAL_MAQUINARIA = (
    ('FU', _("En Funcionamiento")),
    ('RE', _("En Reparación")),
    ('DA', _("Dañado")),
)

## Unidades de medida
UNIDAD_MEDIDA = (
    ('KG',_('Kilogramos')),
    ('TN',_('Toneladas')),
    ('LT',_('Litros')),
    ('MT',_('Metros')),
    ('M2',_('Metros Cuadrados')),
    ('UV',_('Unidad de Venta al Detal')),
)

## Monedas
MONEDAS = (
    ('bsf',_('Bolívares')),
    ('usd',_('Dólares'))
)

## Capacidad Instalada
CAPACIDAD_INSTALADA_MEDIDA = (
    ('','Seleccione...'),("GR","Gramo"),("KG","Kilogramo"),("TN","Tonelada")
)

## Tipo de Tenencia
TIPO_TENENCIA = (
    (1, _("Ocupación")),
    (2,_("Arrendada")),
    (3,_("Comodato")),
    (4,_("Propia")),
    (5,_("Otra"))
)

## Estado del proceso
ESTADO_PROCESO = (
    (1,_("Activo")),
    (0,_("Inactivo"))
)

## Tipo de Proceso
TIPO_PROCESO = (
    ("LN", _("Lineas")),
    ("ET",_("Estaciones de Trabajo")),
    ("OT",_("Otras"))
)

## Tipo de Servicio
TIPO_SERVICIO = (
    ("TN",_("Transporte")),
    ("AL",_("Almacenamiento")),
    ("SE",_("Servicios de Educación")),
    ("SS",_("Servicios de Salud")),
    ("SH",_("Servicios Hoteleros y Turísticos")),
    ("SF",_("Servicios Financieros")),
    ("SC",_("Servicios Sociales y Comunales")),
    ("OT",_("Otros")),
)

# 26 Letras
## Columnas de archivos de carga masiva.
COLUMNS_CM = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z"
]