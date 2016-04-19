from django.core.urlresolvers import reverse
from django.conf import settings

from allauth.account.adapter import DefaultAccountAdapter


class EuroSciPy2016Adapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return settings.LOGIN_REDIRECT_URL

    def get_logout_redirect_url(self, request):
        return settings.LOGOUT_REDIRECT_URL

    def get_email_confirmation_redirect_url(self, request):
        return reverse('account_login')
