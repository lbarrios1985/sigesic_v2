$(document).ready(function(){
    var select = $(".select2");

    if (select.length) {
        /** Instrucción que asigna el estilo select2 a los campos del formulario del tipo select */
        select.select2();
    }
});