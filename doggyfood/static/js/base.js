/**
 * Created by Yuval on 7/7/2016.
 */
$(function () {
        var category = "";
        var compList = "";
        $('.compare-btn .btn-primary').prop('disabled', true);
        $('#checkbox-group').slideUp(0).css('visibility', 'hidden');
        $('input:checkbox').prop('checked', false);
        $('.search-group .checkbox-group').prop('checked', true);
        $('#all').click(function () {
            $('#checkbox-group').slideUp().css('visibility', 'hidden');
            $('#checkbox-group  input:checkbox').prop('checked', true);
        });

        $('#custom').click(function () {
            $('#checkbox-group').slideDown().css('visibility', 'visible');
            $('#checkbox-group  input:checkbox').prop('checked', false);
        });

        var inHover = function () {
            var contentId = '#' + $(this).attr('id');
            var cardId = '#card_' + contentId.split('_')[1];
            var imgId = '#img_' + cardId.split('_')[1];
            var ingNutId = '#ing-nut_' + cardId.split('_')[1];
            var descId = '#desc_' + cardId.split('_')[1];
            var compId = '#check_' + cardId.split('_')[1];
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

        $('.card-content').hover(inHover, exitHover);

        var compHover = function () {
            var cardId = '#' + $(this).attr('id');
            var compId = '#check_' + cardId.split('_')[1];
            $(compId).click(function () {
                if ($(compId).is(':checked')) {
                    compList += cardId.split('_')[1] + ',';
                    var temp = compList.split(',');
                    temp = jQuery.uniqueSort(temp);
                    if (temp.length > 2) {
                        $('.compare-btn .btn-primary').prop('disabled', false);
                    }
                    else {
                        $('.compare-btn .btn-primary').prop('disabled', true);
                    }
                    compList = '';
                    for (var i = 0; i < temp.length; i++) {
                        if (temp[i] != ',' && temp[i] != '') {
                            compList += temp[i] + ',';
                        }
                    }
                }
                else {
                    var temp = compList.split(',');
                    temp = jQuery.uniqueSort(temp);
                    for (var i = 0; i < temp.length; i++) {
                        if (temp[i] === cardId.split('_')[1]) {
                            temp[i] = '';
                            compList.replace(cardId.split('_')[1], '');
                        }
                    }
                    if (temp.length > 2) {
                        $('.compare-btn .btn-primary').prop('disabled', false);
                    }
                    else {
                        $('.compare-btn .btn-primary').prop('disabled', true);
                    }
                    compList = "";

                    for (var i = 0; i < temp.length; i++) {
                        if (temp[i] != ',' && temp[i] != '') {
                            compList += temp[i] + ',';
                        }
                    }

                }
                $('#compare-list-input').val(compList.substr(0, compList.length - 1));
            });
        };

        var compExit = function () {

        };

        $('.card').hover(compHover, compExit);

        $('#checkbox-group input:checkbox').change(function () {
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
    }
);
