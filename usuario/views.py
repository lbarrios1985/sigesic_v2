"""
Sistema Integral de Gestión para la Industria y el Comercio (SIGESIC)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/wiki
"""
## @namespace usuario.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de usuario
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from usuario.forms import AutenticarForm
from usuario.models import UserProfile

import logging

logger = logging.getLogger("usuario")

__licence__ = "GNU Public License v2"
__revision__ = ""
__docstring__ = "DoxyGen"

def acceso(request):
    """!
    Funcion que gestiona el acceso al sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-04-2016
    @param request Objeto que obtiene la peticion
    @return Redirecciona al usuario a la pagina correspondiente en caso de que se haya autenticado o no
    """
    if request.method == "POST":
        form = AutenticarForm(data=request.POST)

        if form.is_valid():
            username = "%s%s%s" % (
                request.POST['tipo_rif'], request.POST['numero_rif'], request.POST['digito_validador_rif']
            )
            usuario = authenticate(username=username, password=str(request.POST['clave']))
            login(request, usuario)
            usr = User.objects.get(username=username)
            usr.last_login = datetime.now()
            usr.save()
            if UserProfile.objects.filter(user=usr):
                # Registra información de conexión del usuario
                profile = UserProfile.objects.get(user=usr)
                profile.conectado = True
                profile.ip = request.META.get('REMOTE_ADDR')
                profile.save()
            logger.info("Acceso al sistema por el usuario [%s]" % username)
            return HttpResponseRedirect(urlresolvers.reverse("inicio"))
        else:
            return render_to_response('acceso.html', {'form': form}, context_instance=RequestContext(request))

    return render_to_response("acceso.html", {'form': AutenticarForm()}, context_instance=RequestContext(request))


def salir(request):
    """!
    Funcion que gestiona la salida del sistema

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 23-04-2016
    @param request Objeto que contiene la peticion
    @return Redirecciona al usuario a la pagina de inicio, si fue desautenticado lo envia a la pagina de acceso
    """
    user = request.user
    if user.is_authenticated():
        logout(request)

        logger.info("El usuario [%s] salio del sistema" % user)

    return HttpResponseRedirect(urlresolvers.reverse("inicio"))