$(document).ready(function () {
    var minHeight = $(window).height() - $('header').height() - $('footer').height();
    $('#main').css('min-height', minHeight + 'px');
});
