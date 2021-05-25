from django.db import models

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils import timezone
# Create your models here.

from multiselectfield import MultiSelectField

from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

from django.contrib.auth.models import PermissionsMixin

from django.db.models import Q
from datetime import timedelta


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # if you require phone number field in your project
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True)  # you can set it unique = True

    class Types(models.TextChoices):
        EMPLOYEE = 'employee', "EMPLOYEE"
        SUPERVISOR = 'supervisor', "SUPERVISOR"
    

    default_type = Types.EMPLOYEE

    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        if not self.id:
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)
     
class SupervisorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.SUPERVISOR))

class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.EMPLOYEE))
class SupervisorAdditional(models.Model):
    user = OneToOneField(CustomUser,on_delete=models.CASCADE)
class EmployeeAdditional(models.Model):
    user = OneToOneField(CustomUser,on_delete=models.CASCADE)
    supervisor = ForeignKey(SupervisorAdditional,on_delete=models.CASCADE)
class Employee(CustomUser):
    default_type = CustomUser.Types.EMPLOYEE
    objects = EmployeeManager()
    class Meta:
        proxy = True
class Supervisor(CustomUser):
    default_type = CustomUser.Types.SUPERVISOR
    objects = SupervisorManager()
    class Meta:
        proxy = True
    @property
    def showAdditional(self):
        return self.supervisoradditional
class Employee(CustomUser):
    default_type = CustomUser.Types.EMPLOYEE
    objects = EmployeeManager()
    class Meta:
        proxy = True
    @property
    def showSupervisor(self):
        return self.employeeadditional

