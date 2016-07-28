"use strict";

$(function () {
    $("#reviewform").submit(function () {
        var form = $(this);
        var data = {
            title: $("#id_title").val(),
            content: $("#id_content").val()
        };
        $.post("", data, function (resp) {
            var el = $(resp);
            $("#reviews").prepend(el);
            form.get(0).reset();
        });
        return false;
    });

    
});
