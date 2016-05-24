/**
 * @brief Función que mide la fortaleza de la contraseña y la muestra en pantalla
 * @param password Cadena de carácteres con la contraseña indicada por el usuario
 */
function passwordStrength(password) {
    var desc = new Array();
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
                className: "btn btn-success btn-sm",
                callback: function() {

                }
            },
            'limpiar': {
                label: BTN_LIMPIAR,
                className: "btn btn-primary btn-sm",
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
    var anho_actual = new Date();
    for (i=ANHO_REGISTRO_INICIAL; i<=anho_actual.getFullYear(); i++) {
        $(modal).find('#anhoregistro').append("<option '" + i + "'>" + i + "</option>");
    }
    $(modal).find('.select2').select2({});
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
                label: BTN_REGISTRAR,
                className: "btn btn-primary btn-sm",
                callback: function() {
                    //Registro de las coordenadas o actualizacion de coordenadas
                }
            },
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        }
    });

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
            source: new ol.source.MapQuest({layer: 'osm'})
        });

        var pointFeature = new ol.Feature(new ol.geom.Point([-65.0000,6.5000]).transform('EPSG:4326', 'EPSG:3857'));

        var vectorLayer = new ol.layer.Vector({
            source: new ol.source.Vector({
                features: [pointFeature]
            })
        });

        var map = new ol.Map({
            interactions: ol.interaction.defaults().extend([new app.Drag()]),
            target: 'map',
            layers: [satellite, osm, vectorLayer],
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
            console.log(evt.coordinate);
            console.log(evt.pixel);
        });

        map.addControl(mousePosition);

        map.on('loadstart', function() {
            cargando.showPleaseWait();
        });

        map.on('loadend', function() {
            cargando.hidePleaseWait();
        });
    });

}

/**
 * @brief Función que habilita los campos dependientes de un select
 * @param opcion Respuesta del usuario según la pregunta
 * @param campo Campo a deshabilitar
 */
function habilitar(opcion, campo){
    if(opcion == "S"){
        $('#'+campo).removeAttr('disabled');
    }else{
        $('#'+campo).attr('disabled', 'disabled');
    }
}

function habilitar1(opcion1, campo1){
    if(opcion1 == "O"){
        $('#'+campo1).removeAttr('disabled');
    }else{
        $('#'+campo1).attr('disabled', 'disabled');
    }
}

