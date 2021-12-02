from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import os
import uuid


class UserManager(BaseUserManager):
    def _create_user(self, email, nickname, password, **extra_fields):
        if not nickname:
            raise ValueError("nickname must be set")
        if not email:
            raise ValueError("email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, nickname, password, **extra_fields)

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, nickname, password, **extra_fields)


def user_profilepic_path(instance, filename):
    id = instance.id
    return os.path.join("profilepic", str(id), filename.lower())


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    nickname = models.CharField(verbose_name="Nickname", max_length=20, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(verbose_name="date joined", default=timezone.now)
    profilepic = models.ImageField(upload_to=user_profilepic_path, default="", blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    @property
    def profilepic_512px(self):
        if self.profilepic:
            urlstr = str(self.profilepic.url)
            newurlstr = urlstr[:-4] + "_512" + urlstr[-4:]
            return newurlstr
        return ""

    @property
    def profilepic_50px(self):
        if self.profilepic:
            urlstr = str(self.profilepic.url)
            newurlstr = urlstr[:-4] + "_50" + urlstr[-4:]
            return newurlstr
        return ""

    @property
    def profilepic_256px(self):
        if self.profilepic:
            urlstr = str(self.profilepic.url)
            newurlstr = urlstr[:-4] + "_256" + urlstr[-4:]
            return newurlstr
        return ""
