$(document).ready(function () {
  // Embed the credit card frame.
  paymill.embedFrame($('#credit-card-fields'), {
    lang: 'en'
  }, function(error) {
    if (error) {
      // Frame could not be loaded, check error object for reason.
      console.log(error.apierror, error.message);
      // Example: "container_not_found"
    } else {
      // Frame was loaded successfully and is ready to be used.
    }
  });

  // Submit handler for payment form.
  var form = $('#payment-form');
  form.on('submit', function(event) {

    // Don't submit the form yet.
    event.preventDefault();

    paymill.createTokenViaFrame({
      amount_int: form.find('.amount-int').val(),
      currency:   form.find('.currency').val()
    }, function(error, result) {
      if (error) {
        // Token could not be created, handle error.
        console.log(error.apierror, error.message);
      } else {
        // Attach token to form and submit it.
        form.find('.token').val(result.token);
        form.off('submit').submit();
      }
    });

  });
});
