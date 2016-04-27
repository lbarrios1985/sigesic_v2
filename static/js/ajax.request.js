/**
 * @brief Función que obtiene datos de la persona asociada al número de rif a consultar
 * @param rif Número de RIF a consultar
 * @param campo_nombre Nombre del campo en donde se mostrará el nombre de la persona del rif consultado
 * @param agente_retencion Indica si se mostrarán datos sobre si es o no agente de retención de IVA
 * @param contribuyente Indica si se mostrarán datos sobre si es o no contribuyente de IVA
 */
function get_data_rif(rif, campo_nombre, agente_retencion, contribuyente) {
    agente_retencion = typeof agente_retencion !== 'undefined' ? agente_retencion : '';
    contribuyente = typeof contribuyente !== 'undefined' ? contribuyente : '';

    if (rif.length == 10) {
        $.getJSON(URL_GET_DATA_RIF, {
            rif: rif, agente_retencion: agente_retencion, contribuyente: contribuyente
        }, function(datos) {
            if (datos.result) {
                $("#"+campo_nombre).val(datos.nombre);
            }
        }).fail(function(jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        });
    }
}

/**
 * @brief Función que valida un número de rif con los registros del SENIAT
 * @param rif Número de RIF a consultar
 */
function validar_rif_seniat(rif) {

}