$(document).ready(function() {

  var windowHeight = $(window).height();
  var footerBottom = $('#footer').offset().top + $('#footer').height();

 if (footerBottom < windowHeight) {
    $('#footer').css('margin-top', '-39px');
  }
});
