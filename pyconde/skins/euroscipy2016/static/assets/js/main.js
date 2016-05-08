jQuery.fn.preventDoubleSubmission = function() {
    var last_clicked, time_since_clicked;
    jQuery(this).bind('submit', function(event) {
        if(last_clicked) {
            time_since_clicked = jQuery.now() - last_clicked;
        }
        last_clicked = jQuery.now();
        if(time_since_clicked < 2000) {
            // console.log("Blocking form submit because it was too soon after the last submit.");
            event.preventDefault();
        }
        // else console.log("submit");
        return true;
    });
};

$(document).ready(function () {
    var minHeight = $(window).height() - $('header').height() - $('footer').height();
    $('#main').css('min-height', minHeight + 'px');

});
