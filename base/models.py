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

class Employee(CustomUser):
    default_type = CustomUser.Types.EMPLOYEE
    objects = EmployeeManager()
    class Meta:
        proxy = True
    @property
    def showSupervisor(self):
        return self.employeeadditional

class EmployeeAdditional(models.Model):
    user = OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="emp")
    supervisor = ForeignKey(Supervisor,on_delete=models.CASCADE,related_name="empsupervisor")

class ExpenseID(models.Model):
    eid = models.CharField(max_length=225)
    epattern = models.CharField(max_length=50)

    def __str__(self):
        return self.eid

class Vendor(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField(unique=True,null=True,blank=True)
    expense_ids = models.ManyToManyField(ExpenseID,null=True,blank=True)

    def __str__(self):
        return self.name

class BillOther(models.Model):
    description = models.CharField(max_length=255)
    is_type_discount = models.BooleanField() #True for discount False for Extra cost
    amount = models.DecimalField(decimal_places=10,max_digits=10)

class Bill(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    invoice_num = models.CharField(max_length=100)
    invoice_date = models.DateField()
    expense_id = models.CharField(max_length=255)
    exp_from_date = models.DateField()
    exp_to_date = models.DateField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10,decimal_places=3)

    amount = models.DecimalField(max_digits=10,decimal_places=3)
    gst = models.DecimalField(max_digits=10,decimal_places=3)
    other=models.ForeignKey(BillOther, on_delete=models.CASCADE,null=True,blank=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=3)

    due_payment = models.DateField()

    def __str__(self):
        return self.invoice_num


class BillImage(models.Model):
    image = models.FileField()
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url


