/**
* Instrucciones a ejecutar al momento de cargar la aplicación
*
* @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
* @copyright GNU/GPLv2
* @date 22-04-2016
*/
$(document).ready(function() {
    /** Declaración de variables */
    var select = $('select'), data_table = $('.dataTable'), refresh_captcha = $('.js-captcha-refresh'),
        input_captcha = $('input[name="captcha_1"]'),
        tip_top = $('.tip-top'), tip_bottom = $('.tip-bottom'), tip_left = $('.tip-left'), tip_right = $('.tip-right');

    if (input_captcha.length) {
        input_captcha.addClass("form-control input-sm");
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

    /** Agrega el estilo para los tooltiptext de los elementos del formulario */
    if (!tip_top.length && !tip_bottom.length && !tip_left.length && !tip_right.length) {
        $('[data-toggle="tooltip"]').tooltip();
    }
    else {

        tip_top.tooltip({
            placement: 'top'
        });
        tip_bottom.tooltip({
            placement: 'bottom'
        });
        tip_left.tooltip({
            placement: 'left'
        });
        tip_right.tooltip({
            placement: 'right'
        });
    }

    if (select.length) {
        /** Instrucción que asigna el estilo select2 a los campos del formulario del tipo select */
        select.select2();
    }
    if (data_table.length) {
        /** Inicializa los elementos del dataTable */
        data_table.dataTable({
            "language": {
                "url": "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
            },
            "ordering": true,
            "order": [[0, 'asc']],
            "bDestroy": true,
            "bPaginate": true,
            "bInfo": true
        });
    }
});