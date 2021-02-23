import uuid

from multiselectfield import MultiSelectField

from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from cities_light.models import Country, Region


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_("Modified At"))

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError("The username must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, password, **extra_fields)


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    GENDER_OPTIONS = (
        ("Male", _("Male")),
        ("Female", _("Female")),
        ("Other", _("Other"))
    )
    SUBSCRIPTION_STATUS = (
        ('Subscribed', _('Subscribed')),
        ('Not Subscribed', _('Not Subscribed')),
    )
    VISIT_REASON = (
        ('Trader', _("I am a Trader.")),
        ('Financial Advisor', _("I'm Financial Advisor.")),
        ('Curious', _("I'm Curious.")),
        ('Other', _("Other Reason.")),
    )

    ROLE = (
        ('admin', _("Admin")),
        ('customer', _("I'm Financial Advisor.")),
        ('Curious', _("I'm Curious.")),
        ('Other', _("Other Reason.")),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("First name"))
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Last name"))
    strip_id = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_OPTIONS, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/', null=True, blank=True, help_text=_("User profile picture"))
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    state = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    visitReason = MultiSelectField(choices=VISIT_REASON)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created At"))
    modified_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_("Modified At"))
    is_staff = models.BooleanField(
        _("staff"),
        default=False,
        help_text=_("Designates whether this user should be treated as staff. "),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts."
        ),
    )

    # User to login into account.
    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        verbose_name_plural = "Users"

    def fullname(self):
        return self.first_name + " " + self.last_name

