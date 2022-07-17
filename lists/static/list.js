// hide .has-error class elements on keypress
var initialize = function () {
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide();
    });
};