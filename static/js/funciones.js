/**
 * @brief Función que mide la fortaleza de la contraseña y la muestra en pantalla
 * @param password Cadena de carácteres con la contraseña indicada por el usuario
 */
function passwordStrength(password) {
    var desc = [];
    desc[0] = MSG_PASSWD_MUY_DEBIL;
    desc[1] = MSG_PASSWD_DEBIL;
    desc[2] = MSG_PASSWD_REGULAR;
    desc[3] = MSG_PASSWD_BUENA;
    desc[4] = MSG_PASSWD_FUERTE;
    desc[5] = MSG_PASSWD_MUY_FUERTE;

    var score   = 0;

    //if password bigger than 6 give 1 point
    if (password.length > 6) score++;

    //if password has both lower and uppercase characters give 1 point
    if ( ( password.match(/[a-z]/) ) && ( password.match(/[A-Z]/) ) ) score++;

    //if password has at least one number give 1 point
    if (password.match(/\d+/)) score++;

    //if password has at least one special caracther give 1 point
    if ( password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/) ) score++;

    //if password bigger than 12 give another 1 point
    if (password.length > 12) score++;

     document.getElementById("passwordDescription").innerHTML = desc[score];
     document.getElementById("passwordStrength").className = "strength" + score;
     document.getElementById("passwordMeterId").value = score;
}

/**
 * @brief Función que muestra una ventana emergente con el formulario de selección para el año de registro
 * @param title Titulo de la ventana emergente
 * @param template Plantilla html a utilizar para mostrar el formulario
 */
function anho_registro(title, template) {
    var modal = bootbox.dialog({
        title: title,
        message: template,
        buttons: {
            success: {
                label: BTN_REGISTRAR,
                className: "btn btn-primary btn-sm",
                callback: function() {

                }
            },
            'limpiar': {
                label: BTN_LIMPIAR,
                className: "btn btn-success btn-sm",
                callback: function() {
                    $(modal).find("form")[0].reset();
                    return false;
                }
            },
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        }
    });

    $(modal).find('#anhoregistro').html("<option value=''>" + SELECT_INICIAL_DATA + "</option>");
    $.getJSON(URL_ANHO_REGISTRO, {}, function(datos) {
        if (datos.resultado) {
            for (i=0;i<datos.anhos.length;i++) {
                $(modal).find('#anhoregistro').append("<option value='" + datos.anhos[i] + "'>" + datos.anhos[i] + "</option>");
            }
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
    $(modal).find('.select2').select2({});
}

/**
 * @brief Función que muestra una ventana emergente con un listado de direcciones
 * @param title Titulo de la ventana emergente
 * @param template Plantilla html a utilizar para mostrar el listado de direcciones
 */
function listado_directorio(title, template) {
    var modal = bootbox.dialog({
        title: title,
        message: template,
        size: 'large',
        buttons: {
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        }
    });
    $(modal).on("shown.bs.modal", function() {
        $(this).find('.dataTable').dataTable({
            "language": {
                "url": URL_DATATABLE_ESPANOL
            },
            "ajax": {
                "processing": false,
                "url": URL_GET_DIRECTORIO,
            },
            "columnDefs": [{
                "targets": -1,
                "data": null,
                "className": 'text-center vertical-align',
                "defaultContent": "<i class='ionicon ion-android-add-circle btn-icon' data-toggle='tooltip' " +
                "                 title='" + TOOLTIP_ADD_DIR + "' " +
                                  "onclick='cargar_direccion($(this).parent().parent().find(\".directorio_id\").val())'></i>"
            },
            {
                "targets": "_all",
                "className": "vertical-align"
            }],
            "ordering": true,
            "order": [[0, 'asc']],
            "bDestroy": true,
            "bPaginate": true,
            "bInfo": true,
            "initComplete": function(settings, json) {
                $('.dataTables_length select').select2();
            }
        });

    });



}

/**
 * @brief Función que muestra una ventana emergente con un mapa para la selección de las coordenadas geográficas
 * @param title Titulo de la ventana emergente
 * @param template Plantilla html a utilizar para mostrar el formulario
 */
function seleccionar_coordenadas(title, template) {
    var modal = bootbox.dialog({
        title: title,
        message: template,
        buttons: {
            success: {
                label: BTN_AGREGAR,
                className: "btn btn-primary btn-sm",
                callback: function() {
                    $("#id_coordenada_0").val($(modal).find("#inputLongitud").val());
                    $("#id_coordenada_1").val($(modal).find("#inputLatitud").val());
                }
            },
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        },
        show: false //Por defecto no se muestra la ventana modal al invocarla para poder cargar el mapa
    });
    $(modal).on("shown.bs.modal", function() {
        /* Carga el mapa cuando la ventana modal es mostrada */
        load_map();
    });
    /* Muestra la ventana de dialogo modal despues de haber cargado el mapa en su correspondiente div */
    $(modal).modal("show");
}

/**
 * @brief Función que carga los datos del mapa a mostrar para la selección de coordenadas geográficas
 */
function load_map() {
    $(document).ready(function() {
        var app = {};

        /**
         * @constructor
         * @extends {ol.interaction.Pointer}
         */
        app.Drag = function() {
            ol.interaction.Pointer.call(this, {
                handleDownEvent: app.Drag.prototype.handleDownEvent,
                handleDragEvent: app.Drag.prototype.handleDragEvent,
                handleMoveEvent: app.Drag.prototype.handleMoveEvent,
                handleUpEvent: app.Drag.prototype.handleUpEvent
            });

            /**
             * @type {ol.Pixel}
             * @private
             */
            this.coordinate_ = null;

            /**
             * @type {string|undefined}
             * @private
             */
            this.cursor_ = 'pointer';

            /**
             * @type {ol.Feature}
             * @private
             */
            this.feature_ = null;

            /**
             * @type {string|undefined}
             * @private
             */
            this.previousCursor_ = undefined;
        };

        ol.inherits(app.Drag, ol.interaction.Pointer);

        /**
         * @param {ol.MapBrowserEvent} evt Map browser event.
         * @return {boolean} `true` to start the drag sequence.
         */
        app.Drag.prototype.handleDownEvent = function(evt) {
            var map = evt.map;

            var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
                return feature;
            });

            if (feature) {
                this.coordinate_ = evt.coordinate;
                this.feature_ = feature;
            }

            return !!feature;
        };

        /**
         * @param {ol.MapBrowserEvent} evt Map browser event.
         */
        app.Drag.prototype.handleDragEvent = function(evt) {
            var deltaX = evt.coordinate[0] - this.coordinate_[0];
            var deltaY = evt.coordinate[1] - this.coordinate_[1];

            var geometry = (this.feature_.getGeometry());
            geometry.translate(deltaX, deltaY);
            $("#inputLongitud").val(evt.coordinate[0]);
            $("#inputLatitud").val(evt.coordinate[1]);

            this.coordinate_[0] = evt.coordinate[0];
            this.coordinate_[1] = evt.coordinate[1];
        };

        /**
         * @param {ol.MapBrowserEvent} evt Event.
         */
        app.Drag.prototype.handleMoveEvent = function(evt) {
            if (this.cursor_) {
                var map = evt.map;
                var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
                    return feature;
                });
                var element = evt.map.getTargetElement();

                if (feature) {
                    if (element.style.cursor != this.cursor_) {
                        this.previousCursor_ = element.style.cursor;
                        element.style.cursor = this.cursor_;
                    }
                } else if (this.previousCursor_ !== undefined) {
                    element.style.cursor = this.previousCursor_;
                    this.previousCursor_ = undefined;
                }
            }
        };

        /**
         * @return {boolean} `false` to stop the drag sequence.
         */
        app.Drag.prototype.handleUpEvent = function() {
            this.coordinate_ = null;
            this.feature_ = null;
            return false;
        };

        var satellite = new ol.layer.Tile({
            source: new ol.source.MapQuest({layer: 'sat'})
        });

        var osm = new ol.layer.Tile({
            source: new ol.source.OSM()
        });

        var iconGeometry = new ol.geom.Point([-65.0000,6.5000]).transform('EPSG:4326', 'EPSG:3857');

        var pointFeature = new ol.Feature({
            geometry: iconGeometry,
            name: 'Mark'
        });

        var iconStyle = new ol.style.Style({
            image: new ol.style.Icon(({
                anchor: [0.5, 15], // Posicion del icono en el eje X Y
                anchorXUnits: 'fraction', // Unidad de medida para el posicionamiento del icon en el eje X
                anchorYUnits: 'pixels', // Unidad de medida para el posicionamiento del icon en el eje X
                //opacity: 0.75,
                src: URL_STATIC_FILES+'img/mark.png',
                // the scale factor
                scale: 1.1 // Tamaño de la imagen de acuerdo a la escala en base al tamaño original
            }))
        });

        pointFeature.setStyle(iconStyle);

        var vectorLayer = new ol.layer.Vector({
            source: new ol.source.Vector({
                features: [pointFeature]
            })
        });

        var map = new ol.Map({
            interactions: ol.interaction.defaults().extend([new app.Drag()]),
            target: 'map',
            layers: [osm, vectorLayer],
            view: new ol.View({
                center: ol.proj.transform([-65.0000,6.5000], 'EPSG:4326', 'EPSG:3857'),
                zoom: 4
            })
       });

        var mousePosition = new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(6),
            projection: 'EPSG:3857',
            target: document.getElementById('myposition'),
            undefinedHTML: '&nbsp;'
        });

        map.on('singleclick', function(evt) {
            $("#inputLongitud").val(evt.coordinate[0]);
            $("#inputLatitud").val(evt.coordinate[1]);
            // Modifica la posición actual del marcador al hacer click sobre un punto en el mapa
            iconGeometry.setCoordinates(evt.coordinate);
            //console.log(evt.pixel);
        });

        map.addControl(mousePosition);

        map.on('loadstart', function() {
            cargando.showPleaseWait();
        });

        map.on('loadend', function() {
            cargando.hidePleaseWait();
        });

        map.updateSize();
    });
}

/**
 * @brief Función que habilita los campos dependientes de un select
 * @param opcion Respuesta del usuario según la pregunta
 * @param campo Campo a deshabilitar
 */
function habilitar(opcion, campo) {
    var elemento = $("#"+campo);
    if (opcion === true || (opcion == "S") || (opcion == "Otro") || (opcion == "1") || (opcion!='')) {
        elemento.removeAttr('readonly');
        elemento.removeAttr('disabled');
    }
    else {
        elemento.attr('readonly', 'readonly');
        elemento.attr('disabled', 'disabled');
        elemento.val("");
    }
}

/**
 * @brief Función que habilita los campos dependientes de un select
 * @param opcion Respuesta del usuario según la pregunta
 * @param campo Campo a deshabilitar
 */
function deshabilitar(opcion, campo, rif_0, rif_1, rif_2) {
    var elemento = $("#"+campo);
    var elemento_0 = $("#"+rif_0);
    var elemento_1 = $("#"+rif_1);
    var elemento_2 = $("#"+rif_2);

    if (opcion == 1) {
        elemento.attr('readonly', 'readonly');
        elemento.val("");
    }
    else {
        elemento.removeAttr('readonly');
        elemento_0.attr('disabled', 'disabled');
        elemento_1.attr('disabled', 'disabled');
        elemento_2.attr('disabled', 'disabled');
        elemento_0.val("");
        elemento_1.val("");
        elemento_2.val("");
    }
}

/**
 * @brief Función para agregar campos a un datatable
 * @param campos Es un arreglo con el id de los campos a agregar en la tabla
 * @param table_id Es un campo con el id de la tabla en la que agregan los campos
 */
function add_field_datatable(campos, table_id){
    var bool = true;
    var new_data = [];
    var t = $(table_id).DataTable();
    var index = t.rows()[0].length;
    var id = '';
    $.each(campos,function(index,value){
        var text = $(value).val();
        
        var form = "<input type='text' id="+value.replace('#','') + "_tb value='" + text + "' " + 
                   "name=" + value.replace('#id_','') + "_tb hidden='true' >";        
        if (text.trim()=='') {
            bool = false
        }
        
        if ($(value+" option:selected").text()) {
            text = $(value+" option:selected").text();
        }
        
        new_data.push(text + form);
    });
    
    if (!bool) {
        var modal = bootbox.dialog({
            title: MSG_TITLE_ALERT,
            message: MSG_EMPTY_FIELDS,
            buttons: {
                main: {
                    label: BTN_ACEPTAR,
                    className: "btn btn-primary btn-sm"
                }
            }
        });
        modal.show();
        new_data = [];

        return false;
    }
    else {
        var exists = false;

        $.each(campos,function(index,value){
            id += $(value).val() + '&';
            $(value).val('');
        });

        $.each($(table_id).find('input[type="hidden"]'), function(index,value){
            if ($(value).val() == id) {
                exists = true;
            }
        });

        if (exists) {
            bootbox.alert( MSG_EXISTS_FIELD );
            return false;
        }

        var buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>';
        buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>';
        buttons += '<input type="hidden" name="id" value="' + id + '" />';
        new_data.push(buttons);
        t.row.add(new_data).draw(false);

        return true;
    }
}

/**
 * @brief Remover dinámicamente campos de una datatable con el id mydtable
 * @param table_id Es un campo con el id de la tabla en la que se eliminaran los campos
 */
function remove_field_datatable(table_id) {
    $(table_id).on('click','.remove_item',function(){
        var t = $(table_id).DataTable();
        var myrow = t.row($(this).parent().closest('tr'));
        var modal = bootbox.dialog({
            title: MSG_TITLE_DELETE_FIELDS,
            message: MSG_CONFIRM_DELETE_FIELDS,
            buttons: {
                success: {
                    label: BTN_ACEPTAR,
                    className: "btn btn-primary btn-sm",
                    callback: function() {
                        myrow.remove().draw( false );
                    }
                },
                main: {
                    label: BTN_CANCELAR,
                    className: "btn btn-warning btn-sm"
                }
            },
        });
        modal.show();
    });
}

/**
 * @brief Actualiza dinámicamente campos de una datatable con el id mydtable
 * @param table_id Es un campo con el id de la tabla en la que se actualizaran los campos
 * @param view Campo que hace referencia al script html que esta en base.form.box.html
 * @param campos Es un array con los campos que se manipularan en el modal
 */
function update_field_datatable(table_id,view,campos) {
    var mensaje = '';
    $(table_id).on('click','.update_item',function(){
        var tr = $(this).parent().closest('tr');
        var t = $(table_id).DataTable();
        mensaje = $(view).html();
        var modal = bootbox.dialog({
        title: MSG_TITLE_UPDATE_FIELDS,
        message: mensaje,
        buttons: {
            success: {
                label: BTN_UPDATE,
                className: "btn btn-primary btn-sm",
                callback: function() {
                    var bool = true;
                    var new_data = [];
                    $.each(campos,function(index,value){
                        var text = $(modal).find(value).val();
                        var form = "<input type='text' id="+value.replace('#','')+"_tb value='"+text+"' name="+value.replace('#id_','')+"_tb hidden='true' >";
                        if((text.trim()==''))
                        {
                            $(modal).find(value).parent().closest('.form-group').addClass('has-error');
                            bool = false
                        }
                        if ($(modal).find(value +" option:selected").text()) {
                            text = $(modal).find(value +" option:selected").text();
                        }
                        new_data.push(text+form);
                    });
                    if (!bool) {
                        bootbox.alert( MSG_INCOMPLTE_FIELDS );
                        return false;
                    }
                    else{
                        var buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>';
                        buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>';
                        new_data.push(buttons);
                        t.row(tr).remove().draw(false);
                        t.row.add(new_data).draw(false);
                    }
                }
            },
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        },
        });
        $.each(tr.find('input'),function(index,value){
            $(modal).find(campos[index]).html($(campos[index]).html());
            $(modal).find(campos[index]).val($(value).val());
        });
        modal.show();
    });
}

/**
 * @brief Función para ocultar campos de una datable
 * @param table_id Es un campo con el id de la tabla en la que se ocultaran los campos
 * @param fields Es un arreglo con el id de los campos a ocultar en la tabla
 */
function default_datatable_field(table_id,fields) {
    var t = $(table_id).DataTable();
    $.each(fields,function(index,value){
       var col = t.column(value);
       col.visible(false);
    });
}

/**
 * @brief Función que verifica la distribucion del capital suscrito
 * @param fields Contiene el identificador del elemento a verificar
 */
function porcentaje_capital_suscrito(fields) {
    var suma = 0;

    $(fields).each(function () {
        suma += parseFloat($(this).val()) || 0;
    });

    if (suma > 100) {
        var mensaje = bootbox.dialog({
            title: MSG_TITLE_ALERT,
            message: MSG_ALERT_CAPITAL_SUSCRITO_EXCEDED,
            buttons: {
                main: {
                    label: BTN_ACEPTAR,
                    className: "btn btn-primary btn-sm"
                }
            }
        });
        mensaje.show();
    }

    var a = $('#id_publico_nacional').val(), b = $('#id_publico_extranjero').val(),
        c = $('#id_privado_nacional').val(), d = $('#id_privado_extranjero').val();

    if (parseFloat(a) + parseFloat(b) + parseFloat(c) + parseFloat(d)  < 100) {
        var error = bootbox.dialog({
            title: MSG_TITLE_ALERT,
            message: MSG_ALERT_CAPITAL_SUSCRITO_TOTAL,
            buttons: {
                main: {
                    label: BTN_ACEPTAR,
                    className: "btn btn-primary btn-sm"
                }
            }
        });
        error.show();
    }
}

/**
 * 
 * @param separador Contiene el símbolo de separación de miles
 * @param period Contiene el símbolo de separación de decimales
 * @returns Devuelve el monto con el separador de miles en caso de ser necesario
 */

function separador_miles(separador, period) {
    var romper = this.toString().split(',');
    var numeric = romper[0];
    var decimal = romper.length > 1 ? period + romper[1] : '';
    var reg = /(\d+)(\d{3})/;
    
    while (reg.test(numeric)) {
        numeric = numeric.replace(reg, '$1' + separador + '$2');
    }
    
    if (decimal.length > 3) {
        var error = bootbox.dialog({
            title: MSG_TITLE_ALERT,
            message: MSG_MAX_DECIMAL,
            buttons: {
                main: {
                    label: BTN_ACEPTAR,
                    className: "btn btn-primary btn-sm"
                }
            }
        });

        error.show();
        d = decimal.replace(/(\d{1})/, '');
        return numeric + d;
    }

    return numeric + decimal;
}

/**
 * @brief Función para desahbilitar un valor seleccionado de una lista en otra
 * @param valor Contiene el id del valor que se desahabilitar
 * @param nombre Recibe un str con el nombre del select
 */
function deshabilitar_opcion(valor, nombre) {
    $(nombre+' option').removeAttr('disabled');
    $(nombre+' option[value="' + valor + '"]').attr('disabled', 'disabled');
    $(nombre).select2({});
}

/**
 * @brief Función para inicializar una DataTable con datos de ajax
 * @param nombre Contiene el nombre del id de la tabla
 * @param url Contiene la url de donde hara el ajax
 */
function init_datatable_ajax(nombre,url) {
    table = $('#'+nombre).DataTable();
    table.rows().draw();
    table.rows().remove().draw();
    $.get(url,function(data){
        $.each(data.data,function(index,value){
            table.row.add(value).draw(false);
        });
    });
}

/**
 * @brief Función para cargar una url que reciba algun párametro
 * @param nombre Contiene el nombre del id de la tabla
 * @param url Contiene la url de donde hara el ajax
 * @param parameter_name Contiene el nombre del párametro
 * @param parameter Contiene el valor del párametro
 */
function before_init_datatable(nombre,url,parameter_name,parameter) {
    if (parameter!='' && parameter_name!='') {
      url += "?" +parameter_name + "=" + parameter;
      init_datatable_ajax(nombre,url);
      $('.modal-backdrop').remove();
    }
    else{
        table = $('#'+nombre).DataTable();
        table.rows().remove().draw();
    }
}

/**
 * @brief Función consultar un ajax que cuenta los registros de un modelo
 * @param aplicacion Contiene el nombre de la aplicación
 * @param modelo Contiene el nombre del modelo a consultar
 * @param argumento Contiene el valor por el que se filtrará
 * @param campo Contiene el nombre del campo por el que se filtrará el argumento
 * @return Regresa los datos
 */
function contar_modelo(aplicacion,modelo,argumento,campo) {
    var datos;
    $.ajax({url:'/ajax/count-model',data:{'aplicacion':aplicacion,'model':modelo,
           'argument':argumento,'field':campo},type:'get',
        success:function(data){
            data = JSON.parse(data);
            datos = data.cantidad;
        },
        error:function(error)
        {
            console.log(error);
            datos = error;
        }
    });
    return datos;
}

/**
 * @brief Función para clonar el valor de un elemento en otro
 * @param valor Contiene el valor que se insertará
 * @param campo Contiene el id/clase del formulario donde se colocará el valor
 */
function clone_value(valor,campo) {
    console.log(valor+" "+campo);
    $(campo).val(valor).change();
}

/**
 * @brief Función para validar si el rif ingresado no es el del usuario loegeado
 * @param id_rif Recibe el id del rif que se desea comprobar
 * @param id_text Recibe el id del campo de texto (si se desea) que se limpiará
 */
function duplicate_rif(id_rif,id_text) {
    //noinspection JSDuplicatedDeclaration
    var id_text = (typeof (id_text) != 'undefined') ? id_text : '';
    var rif_text = '';
    for (i=0; i<=2; i++) {
        rif_text+= $(id_rif+"_"+i).val();
    }
    if (rif_text == RIF){
        var error = bootbox.dialog({
            title: MSG_TITLE_ALERT,
            message: MSG_DUAL_RIF,
            buttons: {
                    main: {
                        label: BTN_ACEPTAR,
                        className: "btn btn-primary btn-sm"
                    }
                }
            });
        error.show()
        //Se limpian los valores
        for (i=1; i<=2; i++) {
            rif_text+= $(id_rif+"_"+i).val("");
        }
        if (id_text!='') {
          $(id_text).val('');
        }
    }
}

/**
 * @brief Función para mostrar el formulario de carga masiva y modificar el boton de descargar archivo
 * @param father_id Contiene el id del padre
 * @param anho_registro_id contiene el id del año de registro
 * @param app Contiene el nombre de la aplicación
 * @param model Contiene el nombre del modelo
 * @param element_show Contiene el nombre del contenedor que se mostrará
 */
function mostrar_carga(father_id,anho_registro_id,app,model,element_show) {
    var element = $(element_show);
    if (father_id!='' && anho_registro_id!='') {
        $('#descargar_archivo-'+model).attr("onclick","cm_descargar_archivo('"+app+"','"+model+"','"+anho_registro_id+"','"+father_id+"')");
        if (element.attr('style')=='display: none;') {
            element.show();
        }
    }
    else if (father_id!='' || anho_registro_id!='') {
        if (element.attr('style')!='display: none;') {
            element.hide();
        }
    }
    
}

/**
 * @brief Función para mostrar el formulario de carga masiva y modificar el boton de descargar archivo
 * @param father_id Contiene el id del padre
 * @param anho_registro_id contiene el id del año de registro
 * @param app Contiene el nombre de la aplicación
 * @param model Contiene el nombre del modelo
 * @param element_show Contiene el nombre del contenedor que se mostrará
 */
function mostrar_carga_producto_cliente(father_id,anho_registro_id,app,model,element_show,oculto_producto) {
    var element = $(element_show);
    var producto=$(oculto_producto);
    console.log(element);
    $(document).ready(function()
    {
        $("input[name=carga]").on('change',function () {
            if (model=="Produccion"){
            var opc=$(this).val();
            if (father_id!='' && anho_registro_id!='' && opc=="Carga_Masiva"){
                $('#descargar_archivo-'+model).attr("onclick","cm_descargar_archivo('"+app+"','"+model+"','"+anho_registro_id+"','"+father_id+"')");
                element.show();
                producto.hide();
            }
            else if (father_id!='' && anho_registro_id!='' && opc=="Carga_Formulario"){
                producto.show();
                element.hide();
            }
            else{
                producto.hide();
                element.hide();
            }
        }
        });

        $("input[name=carga1]").on('change',function () {
            if (model=="FacturacionCliente"){
            var opc=$(this).val();
            if (father_id!='' && anho_registro_id!='' && opc=="Carga_Masiva"){
                $('#descargar_archivo-'+model).attr("onclick","cm_descargar_archivo('"+app+"','"+model+"','"+anho_registro_id+"','"+father_id+"')");
                element.show();
                producto.hide();
            }
            else if (father_id!='' && anho_registro_id!='' && opc=="Carga_Formulario"){
                producto.show();
                element.hide();
            }
            else{
                producto.hide();
                element.hide();
            }

        }
        });

    });
}


/**
 * @brief Función para traerse el número de clientes/proveedores faltantes por llenar
 * @param attr Contiene el valor del campo
 * @param app Contiene el nombre de la aplicación
 * @param model Contiene el nombre del argumento
 * @param field Recibe el campo
 * @param value Recibe el valor
 * @param field_id Recibe el id del campo donde se harán los cambios
 * @param other_app Recibe la otra aplicacion
 * @param other_model Recibe el modelo para contar
 * @param filter Recibe el filtro del modelo para contar
 * @param name Recibe nombre(cliente/proveedor)
 * @param nota Recibe el id del div donde colocará la nota
 */
function get_cliente_proveedor(attr,app,model,field,value,field_id,other_app,other_model,filter,name,nota) {
    //noinspection JSDuplicatedDeclaration
    var nota = (typeof (nota) != 'undefined') ? nota : '#nota';
    if (attr!='') {
        $.ajax({url:'/ajax/cliente-data',data:{'aplicacion':app,'model':model,'argument':attr,
               'field':field,'value':value},type:'get',
            success:function(data){
                data = JSON.parse(data);
                var contar = contar_modelo(other_app,other_model,attr,filter);
                if (parseInt(contar)<parseInt(data.model)) {
                    var capital_letter = name.replace(/\b[a-z]/g,function(f){return f.toUpperCase();});
                    $(nota).text('');    
                    $(field_id).val(capital_letter+" # "+(contar+1));
                    $(nota).text('Faltan '+(parseInt(data.model)-parseInt(contar))+' '+name+'(s)');
                }
                else{
                    $(nota).text("No debe ingresar más "+name+"s");
                }
            },
            error:function(error)
            {
                console.log(error);
            }
        });
    }
}

/**
 * @brief Función para permitir sólo números
 * @param elem Recibe el elemento como tal
 */
function only_numbers(elem) {
    $(elem).val($(elem).val().replace(/[^0-9]/g,''));
}

/**
 * @brief Función para permitir sólo números y una coma
 * @param elem Recibe el elemento como tal
 */
function only_numbers_comma(elem) {
    $(elem).val($(elem).val().replace(/[^0-9\,]/g,'').replace(/(,.*?),(.*,)?/, "$1"));
}
