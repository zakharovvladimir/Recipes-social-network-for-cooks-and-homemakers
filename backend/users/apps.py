"""Users apps."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Users app activation."""

    name = 'users'
    verbose_name = _('Users')
