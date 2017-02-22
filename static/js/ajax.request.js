/**
 * @brief Función que obtiene datos de la persona asociada al número de rif a consultar
 * @param campo_rif Nombre del campo del RIF a consultar
 * @param campo_nombre Nombre del campo en donde se mostrará el nombre de la persona del rif consultado
 * @param registro Indica si la validación realizada es en el formulario de registro
 * @param agente_retencion Indica si se mostrarán datos sobre si es o no agente de retención de IVA
 * @param contribuyente Indica si se mostrarán datos sobre si es o no contribuyente de IVA
 */
function get_data_rif(campo_rif, campo_nombre, registro, agente_retencion, contribuyente) {
    agente_retencion = typeof agente_retencion !== 'undefined' ? agente_retencion : '';
    contribuyente = typeof contribuyente !== 'undefined' ? contribuyente : '';
    registro = typeof registro !== 'undefined' ? registro : false;

    var rif = '', datos_usuario = $(".datos-usuario");

    for (i=0; i<=2; i++) {
        sufix = i;
        rif += $("#" + campo_rif + "_" + sufix.toString()).val();
    }

    if (rif.length == 10) {
        $.getJSON(URL_GET_DATA_RIF, {
            rif: rif, agente_retencion: agente_retencion, contribuyente: contribuyente
        }, function(datos) {

            if (datos.result) {
                if (typeof datos.error_message !== 'undefined') {
                    bootbox.alert(datos.error_message);
                }
                $("#"+campo_nombre).val(datos.nombre);
                if (registro) {
                    datos_usuario.show();
                }
            }
            else {
                datos_usuario.hide();
                bootbox.alert(datos.message);
            }
        }).fail(function(jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        });
    }
}

/**
 * @brief Función que valida un número de rif con los registros del SENIAT
 * @param campo_rif Nombre del campo del RIF a consultar
 * @param campo_nombre Nombre del campo en donde se mostrará el nombre de la persona del rif consultado
 * @param registro Indica si la validación realizada es en el formulario de registro
 * @param agente_retencion Indica si se mostrarán datos sobre si es o no agente de retención de IVA
 * @param contribuyente Indica si se mostrarán datos sobre si es o no contribuyente de IVA
 */
function validar_rif_seniat(campo_rif, campo_nombre, registro, agente_retencion, contribuyente) {
    agente_retencion = typeof agente_retencion !== 'undefined' ? agente_retencion : '';
    contribuyente = typeof contribuyente !== 'undefined' ? contribuyente : '';
    registro = typeof registro !== 'undefined' ? registro : false;

    var rif = '', tipo_rif_list = ["V", "E", "J", "P"], tipo_rif = $("#" + campo_rif + "_0").val(),
        numero_rif = $("#" + campo_rif + "_1").val(), digito_rif = $("#" + campo_rif + "_2").val();

    for (i=0; i<=2; i++) {
        sufix = i;
        rif += $("#" + campo_rif + "_" + sufix.toString()).val();
    }

    if (tipo_rif != "" && numero_rif != "" && digito_rif != "") {
        if (rif.length < 10 || rif.length > 10) {
            bootbox.alert( MSG_LENGTH_RIF );
        }
        else if (isNaN(parseInt(numero_rif)) || isNaN(parseInt(digito_rif))) {
            bootbox.alert( MSG_RIF_INCORRECTO );
        }
        else if (tipo_rif_list.indexOf(tipo_rif) < -1) {
            bootbox.alert( MSG_TIPO_RIF );
        }
        else {
            $.getJSON(URL_VALIDAR_RIF_SENIAT, {rif: rif}, function(datos) {
                if (datos.result) {
                    get_data_rif(campo_rif, campo_nombre, registro, agente_retencion, contribuyente);
                }
                else {
                    bootbox.alert(datos.message);
                }
            }).fail(function(jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
            });
        }
    }

}

/**
 * @brief Función que elimina registros del sistema
 * @param url Dirección URL de la función que atiende la petición para la eliminación de registros
 * @param label Etiqueta de la aplicación del modelo a eliminar
 * @param modelo Modelo en el cual se eliminarán datos
 * @param id Identificador del registro a eliminar
 */
function eliminar_registro(url, label, modelo, id) {
    bootbox.confirm(MSG_ELIMINAR_REGISTRO, function(result) {
        if (result) {
            $.getJSON(url, {app_label: label, modelo: modelo, id: id}, function (datos) {
                var msg = "";
                if (datos.resultado) {
                    msg = MGS_REGISTRO_ELIMINADO;
                }
                else {
                    msg = MSG_REGISTRO_NO_ELIMINADO;
                }
                bootbox.alert(msg, function() {
                    console.log(msg);
                    location.reload();
                });
            }).fail(function(jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
                console.log(MSG_PETICION_AJAX_FALLIDA + err)
            });
        }
    });
}

/**
 * @brief Función que actualiza los datos de combos dependientes
 * @param opcion Código del elemento seleccionado por el cual se filtrarán los datos en el combo dependiente
 * @param app Nombre de la aplicación en la cual buscar la información a filtrar
 * @param mod Modelo del cual se van a extraer los datos filtrados según la selección
 * @param campo Nombre del campo con el cual realizar el filtro de los datos
 * @param n_value Nombre del campo que contendra el valor de cada opción en el combo
 * @param n_text Nombre del campo que contendrá el texto en cada opción del combo
 * @param combo_destino Identificador del combo en el cual se van a mostrar los datos filtrados
 * @param bd Nombre de la base de datos, si no se específica se asigna el valor por defecto
 */
function actualizar_combo(opcion, app, mod, campo, n_value, n_text, combo_destino, bd) {
    /* Verifica si el parámetro esta definido, en caso contrario establece el valor por defecto */
    bd = typeof bd !== 'undefined' ? bd : 'default';
    $.ajaxSetup({
        async: false
    });
    $.getJSON(URL_ACTUALIZAR_SELECT, {
        opcion:opcion, app:app, mod:mod, campo:campo, n_value:n_value, n_text: n_text, bd:bd
    }, function(datos) {

        var combo = $("#"+combo_destino);

        if (datos.resultado) {

            if (datos.combo_disabled == "false") {
                combo.removeAttr("disabled");
            }
            else {
                combo.attr("disabled", "true");
            }

            combo.html(datos.combo_html);
        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        console.log(MSG_PETICION_AJAX_FALLIDA + err)
    });
}

/**
 * @brief Función que permite cargar los datos de un combo
 * @param app Nombre de la aplicación en la cual buscar la información a filtrar
 * @param mod Modelo del cual se van a extraer los datos filtrados según la selección
 * @param n_value Nombre del campo que contendra el valor de cada opción en el combo
 * @param n_text Nombre del campo que contendrá el texto en cada opción del combo
 * @param id_combo Identificador del combo en el cual se van a mostrar los datos filtrados
 * @param bd Nombre de la base de datos, si no se específica se asigna el valor por defecto
 */
function cargar_combo(app, mod, n_value, n_text, id_combo, bd) {
    bd = typeof bd !== 'undefined' ? bd : 'default';
    $.getJSON(URL_CARGAR_COMBO, {app:app, mod:mod, n_value:n_value, n_text:n_text, bd:bd}, function(datos) {
        var combo = $("#"+id_combo);
        if (datos.resultado) {
            combo.html(datos.combo_html);
        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        console.log(MSG_PETICION_AJAX_FALLIDA + err)
    });
}

/**
 * @param directorio_id Identificador del directorio a cargar
 */
function cargar_direccion(directorio_id) {

    $.getJSON(URL_ADD_DIRECCION, {directorio_id: directorio_id}, function(datos) {
        if (datos.resultado) {
            var directorio = $("#id_directorio"), tipo_vial = $("#id_tipo_vialidad"),
                nombre_vial = $("#id_nombre_vialidad"), tipo_edif = $("#id_tipo_edificacion"),
                desc_edif = $("#id_descripcion_edificacion"), tipo_subedif = $("#id_tipo_subedificacion"),
                desc_subedif = $("#id_descripcion_subedificacion"), tipo_zona = $("#id_tipo_zonificacion"),
                nombre_zona = $("#id_nombre_zona"), estado = $("#id_estado"), municipio = $("#id_municipio"),
                parroquia = $("#id_parroquia"), coor_0 = $("#id_coordenada_0"),
                coor_1 = $("#id_coordenada_1");
            directorio.val(directorio_id);
            tipo_vial.find("input[name='tipo_vialidad']").each(function() {
                if ($(this).val() == datos.tipo_vialidad) {
                    $(this).attr('checked', true);
                }
            });
            nombre_vial.val(datos.nombre_vialidad);

            tipo_edif.find("input[name='tipo_edificacion']").each(function() {
                if ($(this).val() == datos.tipo_edificacion) {
                    $(this).attr('checked', true);
                }
            });
            desc_edif.val(datos.descripcion_edificacion);

            tipo_subedif.find("input[name='tipo_subedificacion']").each(function() {
                if ($(this).val() == datos.tipo_subedificacion) {
                    $(this).attr('checked', true);
                }
            });
            desc_subedif.val(datos.descripcion_subedificacion);

            tipo_zona.find("input[name='tipo_zonificacion']").each(function() {
                if ($(this).val() == datos.tipo_zonificacion) {
                    $(this).attr('checked', true);
                }
            });
            nombre_zona.val(datos.nombre_zona);
            estado.val(datos.estado).prop('selected', 'selected').change();
            municipio.val(datos.municipio).prop('selected', 'selected').change();
            municipio.parent().find('.error-notice').remove();
            municipio.parent().parent().removeClass('has-error');
            parroquia.val(datos.parroquia).prop('selected', 'selected').change();
            parroquia.parent().find('.error-notice').remove();
            parroquia.parent().parent().removeClass('has-error');

            if (datos.coordenadas[0]!='' || datos.coordenadas[1]) {
                coor_0.val(datos.coordenadas[0]);
                coor_1.val(datos.coordenadas[1]);
            }

        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).done(function () {
        /* Cierra las ventanas modales generadas despues de agregar la direccion */
        $('.bootbox').modal('hide');
        $("#mensaje_espera").modal('hide');
        $('.modal-backdrop').remove();
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        console.log(MSG_PETICION_AJAX_FALLIDA + err)
    })
}

function cm_descargar_archivo(app, mod, anho, rel_id) {
    anho = typeof anho !== 'undefined' ? anho : '';
    rel_id = typeof rel_id !== 'undefined' ? rel_id : '';
    $.getJSON(URL_DESCARGAR_ARCHIVO_CM, {app:app, mod:mod, anho:anho, rel_id:rel_id}, function(datos) {
        if (datos.resultado) {
            bootbox.alert(datos.message);
            //filename = URL_RETORNAR_ARCHIVO_CM+'?nombre='+datos.archivo+'.xls';
            filename = URL_OPEN_FILE_CM+'/'+datos.archivo+'.xls';
            window.location = filename;
            //window.open(URL_RETORNAR_ARCHIVO_CM+'?nombre='+datos.archivo+'.xls');
        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        console.log(MSG_PETICION_AJAX_FALLIDA + err)
    });
}
