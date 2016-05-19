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
        var satellite = new ol.layer.Tile({
            source: new ol.source.MapQuest({layer: 'sat'})
        });

        var osm = new ol.layer.Tile({
            source: new ol.source.MapQuest({layer: 'osm'})
        });

        satellite.on('tileloadstart', function() {
            cargando.showPleaseWait();
        });

        satellite.on('tileloadend', function() {
            cargando.hidePleaseWait();
        });

        var map = new ol.Map({
            target: 'map',
            layers: [satellite, osm],
            view: new ol.View({
                center: ol.proj.transform([-65.0000,6.5000], 'EPSG:4326', 'EPSG:900913'),
                zoom: 4
            })
        });

        var mousePosition = new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(6),
            projection: 'EPSG:4326',
            target: document.getElementById('myposition'),
            undefinedHTML: '&nbsp;'
        });

        map.addControl(mousePosition);

        map.on("click", function(evt) {

            // agregar funcionalidad para el marcador

            /*iconFeatures = [];
            var iconFeature = new ol.Feature({
              geometry: new ol.geom.Point(ol.proj.transform(evt.coordinate, 'EPSG:4326',
              'EPSG:900913'))
            });

            iconFeatures.push(iconFeature);

            var vectorSource = new ol.source.Vector({
              features: iconFeatures //add an array of features
            });

            var iconStyle = new ol.style.Style({
              image: new ol.style.Icon(({
                anchor: [0.5, 46],
                anchorXUnits: 'fraction',
                anchorYUnits: 'pixels'
              }))
            });


            var vectorLayer = new ol.layer.Vector({
              source: vectorSource,
              style: iconStyle
            });*/
        });
    });

}
