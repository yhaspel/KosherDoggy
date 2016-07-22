/**
 * Created by Yuval on 7/7/2016.
 */
$(function () {
        var category = "";
        var searchText = "";

        $('.compare-btn .btn-primary').prop('disabled', true);
        $('#checkbox-group').slideUp(0).css('visibility', 'hidden');
        $('input:checkbox').prop('checked', false);
        $('.search-group .checkbox-group').prop('checked', true);
        $('#show-filter-btn').click(function () {
            var btnText = $(this).html();
            if (btnText === 'Show Filters') {
                $('#show-filter-btn').html('Hide Filters');
                $('#checkbox-group').stop(true).slideDown().css('visibility', 'visible');
                $('#checkbox-group  input:checkbox').prop('checked', false);
            }
            else {
                $('#show-filter-btn').html('Show Filters');
                $('#checkbox-group').stop(true).slideUp().css('visibility', 'hidden');
                $('#checkbox-group  input:checkbox').prop('checked', true);
            }
        });

        $('#search-box').on('change', function () {
            searchText = $('#search-box').val();
        });

        $('#search-box').focusin(function () {
            searchText = $('#search-box').val();
            $('#search-box').val('');
        });

        $('#search-box').focusout(function () {
            $('#search-box').val(searchText.split(';')[0]);
        });

        var revealCardInfo = function () {
            var currId = '#' + $(this).attr('id');
            if ($(this).attr('class') === 'glyphicon glyphicon-chevron-up') {
                $(this).attr('class', 'glyphicon glyphicon-chevron-down')
                var contentId = '#content_' + currId.split('_')[1];
                var imgId = '#img_' + currId.split('_')[1];
                var ingNutId = '#ing-nut_' + currId.split('_')[1];
                var descId = '#desc_' + currId.split('_')[1];
                // var compId = '#check_' + cardId.split('_')[1];
                $(imgId).stop(true).slideUp(300);
                $(contentId).css('height', '95%');
                $(ingNutId).css('height', '20%');
                $(descId).css('height', '20%');
            }
            else {
                $(this).attr('class', 'glyphicon glyphicon-chevron-up')
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
            }

        };

        var cardHoverIn = function () {
            var cardId = '#' + $(this).attr('id');
            var cardReveal = '#card-reveal_' + cardId.split('_')[1];
            $(cardReveal).click(revealCardInfo)
        };

        $('.card').hover(cardHoverIn)


        $('.compare-check').click(function () {
            var checked = $('.check-compare input:checked').length
            if (checked > 1) {
                var btnText = 'Compare ' + checked + ' Products'
                $('#compare-submit').html(btnText);
                $('#compare-submit').prop('disabled', false);
            }
            else {
                $('#compare-submit').html('Compare');
                $('#compare-submit').prop('disabled', true);
            }
        });

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
