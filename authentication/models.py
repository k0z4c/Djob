from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager

from django.urls import reverse
from django.core.mail import send_mail
from guardian.mixins import GuardianUserMixin

from django.core.validators import EmailValidator
# from django.contrib.auth.validators import EmailValidator

# forms to extend or rewrite: UserCreationForm, UserChangeForm
class User(AbstractBaseUser, PermissionsMixin, GuardianUserMixin):

    email = models.EmailField(_('email address'), unique=True, validators=[EmailValidator])
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
            _('active'),
            default=True,
            help_text=_(
                'Designates whether this user should be treated as active. '
                'Unselect this instead of deleting accounts.'
            ),
        )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super(AbstractBaseUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('account:profile_detail', args=[self.email])

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
