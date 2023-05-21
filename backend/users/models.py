"""Users models.py."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User model."""

    email = models.EmailField(
        max_length=200,
        verbose_name=_('E-mail'),
        unique=True,
        blank=False,
        error_messages={
            'unique': _('Such user exists.'),
        },
        help_text=_('Add your e-mail.'),
    )
    username = models.CharField(
        max_length=200,
        verbose_name=_('Login'),
        unique=True,
        error_messages={
            'unique': _('Such user exists'),
        },
        help_text=_('Add your username'),
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name=_('Name'),
        blank=True,
        help_text=_('Add your name'),
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name=_('Surname'),
        blank=True,
        help_text=_('Add your surname'),
    )
    password = models.CharField(
        max_length=200,
        verbose_name=_('Password'),
        help_text=_('Add your password'),
    )

    class Meta:
        """User Meta."""

        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        """Str."""
        return self.get_full_name()


class Follow(models.Model):
    """Follow model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=_('Подписчик'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Author'),
    )

    class Meta:
        """Follow Meta."""

        verbose_name = _('Subscribe')
        verbose_name_plural = _('Subscribes')
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='self_follow',
            ),
        )

    def __str__(self):
        """Str."""
        return f'{self.user} - {self.author}'
