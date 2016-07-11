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

    var inHover = function () {
        var cardId = '#' + $(this).attr('id');
        var imgId = '#img_' + cardId.split('_')[1];
        var contentId = '#content_' + cardId.split('_')[1];
        var ingNutId = '#ing-nut_' + cardId.split('_')[1];
        var descId = '#desc_' + cardId.split('_')[1];
        $(imgId).slideUp(300);
        $(contentId).css('height', '95%');
        $(ingNutId).css('height', '20%');
        $(descId).css('height', '20%');
    };

    var exitHover = function () {
        var cardId = $(this).attr('id');
        var imgId = '#img_' + cardId.split('_')[1];
        var contentId = '#content_' + cardId.split('_')[1];
        var ingNutId = '#ing-nut_' + cardId.split('_')[1];
        var descId = '#desc_' + cardId.split('_')[1];
        $(contentId).css('height', '55%');
        $(imgId).slideDown(300);
        $(contentId).css('height', '55%');
        $(ingNutId).css('height', '30%');
        $(descId).css('height', '33%');
    };

    $('.card').hover(inHover, exitHover);

    $('input:checkbox').change(function () {
        if ($(this).is(':checked')) {
            category += $(this).val() + ',';
        }
        else {
            var temp = category.split(',');
            for (var i = 0; i < temp.length; i++) {
                if (temp[i] === $(this).val()) {
                    temp[i] = '';
                    category.replace($(this).val(), '');
                }
            }

            category = "";

            for (var i = 0; i < temp.length; i++) {
                if (temp[i] != ',' && temp[i] != '') {
                    category += temp[i] + ',';
                }
            }

        }
        $('#category-select').val(category.substr(0, category.length - 1));
    });
});
