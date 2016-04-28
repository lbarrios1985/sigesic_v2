/**
 * @brief Función que obtiene datos de la persona asociada al número de rif a consultar
 * @param campo_rif Nombre del campo del RIF a consultar
 * @param campo_nombre Nombre del campo en donde se mostrará el nombre de la persona del rif consultado
 * @param agente_retencion Indica si se mostrarán datos sobre si es o no agente de retención de IVA
 * @param contribuyente Indica si se mostrarán datos sobre si es o no contribuyente de IVA
 */
function get_data_rif(campo_rif, campo_nombre, agente_retencion, contribuyente) {
    agente_retencion = typeof agente_retencion !== 'undefined' ? agente_retencion : '';
    contribuyente = typeof contribuyente !== 'undefined' ? contribuyente : '';

    var rif = '';

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

/**
 * @brief Función que valida un número de rif con los registros del SENIAT
 * @param campo_rif Nombre del campo del RIF a consultar
 * @param campo_nombre Nombre del campo en donde se mostrará el nombre de la persona del rif consultado
 * @param agente_retencion Indica si se mostrarán datos sobre si es o no agente de retención de IVA
 * @param contribuyente Indica si se mostrarán datos sobre si es o no contribuyente de IVA
 */
function validar_rif_seniat(campo_rif, campo_nombre, agente_retencion, contribuyente) {
    agente_retencion = typeof agente_retencion !== 'undefined' ? agente_retencion : '';
    contribuyente = typeof contribuyente !== 'undefined' ? contribuyente : '';

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
                    get_data_rif(campo_rif, campo_nombre, agente_retencion, contribuyente);
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