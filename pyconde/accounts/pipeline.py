"""
This holds extensions to social_auth's pipeline.
"""
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from userprofiles.contrib.emailverification.models import EmailVerification


def show_request_email_form(request, user, **kwargs):
    """
    If the user doesn't have an email associated and there is no email
    activation pending, ask the user to add an email to his/her account.
    """
    if user.email or EmailVerification.objects.get_pending(user):
        return
    session_key = '_email_passed_{0}'.format(user.pk)
    if session_key not in request.session:
        return HttpResponseRedirect(reverse('login-email-request'))
    else:
        del request.session[session_key]
