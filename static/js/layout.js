/**
* Instrucciones a ejecutar al momento de cargar la aplicación
*
* @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
* @copyright GNU/GPLv2
* @date 22-04-2016
*/
$(document).ready(function() {
    /** Declaración de variables */
    var browserName = navigator.appName, browserVer = navigator.appVersion, date = new Date(),
        year_info_develop = $("#year-info-develop"), select = $('select'), data_table = $('.dataTable'),
        refresh_captcha = $('.js-captcha-refresh'), input_captcha = $('input[name="captcha_1"]'),
        email_mask = $('.email-mask'), form_update = $('.form-update'), tip_top = $('.tip-top'),
        tip_bottom = $('.tip-bottom'), tip_left = $('.tip-left'), tip_right = $('.tip-right'),
        seleccion_si_no = $('input[type="checkbox"].seleccion_si_no'), file_input = $('input[type="file"]');

    if (browserName.indexOf("Internet Explorer") > -1) {
        /** Verifica el tipo de navegador utilizado por el usuario */
        bootbox.alert(MSG_WEB_NAVIGATOR, function() {
            window.location.href = 'http://www.mozilla-europe.org/es/firefox/';
        });
    }

    if (year_info_develop.length) {
        year_info_develop.html(date.getFullYear());
    }

    if (form_update.length) {
        /** Muestra un mensaje de confirmacion para actualizar datos en el sistema */
        form_update.submit(function(e) {
            var currentForm = this;
            e.preventDefault();
            bootbox.confirm(MSG_REGISTRO_UPDATE, function(result) {
                if (result) {
                    currentForm.submit();
                }
            });
        });
    }

    if (input_captcha.length) {
        /** Agrega clases de bootstrap para el input del captcha */
        input_captcha.addClass("form-control input-sm");

        /** Agrega un placeholder al input del captcha */
        input_captcha.attr("placeholder", "texto de la imagen");
    }

    if (refresh_captcha.length) {
        /** Actualiza la imagen captcha del formulario */
        refresh_captcha.click(function(){
            $form = $(this).parents('form');
            var url = location.protocol + "//" + window.location.hostname + ":" + location.port + "/captcha/refresh/";

            $.getJSON(url, {}, function(json) {
                $form.find('input[name="captcha_0"]').val(json.key);
                $form.find('img.captcha').attr('src', json.image_url);
            });

            return false;
        });
    }

    /** Convierte un campo CheckBox en Switch */
    if (seleccion_si_no.length) {
        seleccion_si_no.bootstrapSwitch({
            onText: 'SI', offText: 'NO', offColor: 'danger', size: 'mini'
        });
        seleccion_si_no.on('switchChange.bootstrapSwitch', function (event, state) {
            $(this).prop( "checked", state );
        });
    }

    /** Agrega el estilo para los tooltiptext de los elementos del formulario */
    if (!tip_top.length && !tip_bottom.length && !tip_left.length && !tip_right.length) {
        $('[data-toggle="tooltip"]').tooltip();
    }
    else {

        tip_top.tooltip({
            placement: 'top'
            //delay: {show: 200, hide:1500}
        });
        tip_bottom.tooltip({
            placement: 'bottom'
            //delay: {show: 200, hide:1500}
        });
        tip_left.tooltip({
            placement: 'left'
            //delay: {show: 200, hide:1500}
        });
        tip_right.tooltip({
            placement: 'right'
            //delay: {show: 200, hide:1500}
        });
    }

    if (select.length) {
        /** Instrucción que asigna el estilo select2 a los campos del formulario del tipo select */
        select.select2();
    }

    if (data_table.length) {
        $.extend( $.fn.dataTableExt.oStdClasses, {
            "sFilterInput": "form-control",
            "sLengthSelect": "form-control select2"
        });
        /** Inicializa los elementos del dataTable */
        data_table.dataTable({
            "language": {
                "url": URL_DATATABLE_ESPANOL
            },
            "ordering": true,
            "order": [[0, 'asc']],
            "bDestroy": true,
            "bPaginate": true,
            "bInfo": true,
            "initComplete": function(settings, json) {
                $('.dataTables_length select').select2();
            }
        });
    }

    if (email_mask.length) {
        /** Crea la respectiva maskara a implementar en los campos de correo electrónico */
        email_mask.mask('A', {translation: {
            "A": {pattern: /[\w@\-.+]/, recursive: true}
        }});
    }

    if (file_input.length) {
        file_input.fileinput({
            language: 'es',
            mainClass: "input-group-sm",
            browseClass: 'btn btn-primary btn-sm btn_accion',
            browseIcon: '<i class="ion-ios-cloud-upload"></i>&nbsp;',
            browseLabel: 'Cargar Archivo'
        });
    }
});