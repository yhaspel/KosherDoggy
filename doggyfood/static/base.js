/**
 * Created by Yuval on 7/7/2016.
 */
$(function () {
    var category = "";
    $('#checkbox-group').slideUp(0).css('visibility', 'hidden');
    $('input:checkbox').prop('checked', true);
    $('#all').click(function () {
        $('#checkbox-group').slideUp().css('visibility', 'hidden');
        $('input:checkbox').prop('checked', true);
    });

    $('#custom').click(function () {
        $('#checkbox-group').slideDown().css('visibility', 'visible');
        $('input:checkbox').prop('checked', false);
    });

    $('input:checkbox').change(function () {
        if ($(this).is(':checked')) {
            category += $(this).val() + ',';
        }
        else {
            var temp = category.split(',');
            for (var i = 0; i < temp.length; i++) {
                if (temp[i] === $(this).val()) {
                    temp[i] = '';
                    category.replace($(this).val(),'');
                }
            }

            category = "";

            for (var i = 0; i < temp.length; i++) {
                if (temp[i] != ',' && temp[i] != '') {
                    category += temp[i] + ',';
                }
            }

        }
        $('#category-select').val(category.substr(0,category.length-1));
    });
});
