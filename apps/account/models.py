import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

#custom user model

class User(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(
        max_length=20, choices=Types.choices
    )
    user_id = models.AutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username


class CustomerProfile(models.Model):
    class GenderType(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'FeMale'
        OTHERS = 'OTHERS', 'Others'

    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='account/images/', default=None)
    phone_number = models.CharField(max_length=14, default="+8801836541269")
    gender = models.CharField(
        max_length=20, choices=GenderType.choices, default=GenderType.MALE
        )
    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
        )
    shipping_address = models.TextField(default="Write your shipping Address")
    billing_address = models.TextField(default="Write your billing Address")
    
    def __str__(self):
        return self.customer.username


class SellerProfile(models.Model):
    class GenderType(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'FeMale'
        OTHERS = 'OTHERS', 'Others'

    seller = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
        )
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='account/images/', default=None)
    phone_number = models.CharField(max_length=14, default="+8801836541269")
    gender = models.CharField(
        max_length=20, choices=GenderType.choices, default=GenderType.MALE
        )
    about_company = models.TextField(
        verbose_name=_("About Company"), default="say something about yourself"
        )
    address = models.TextField(default="Address")

    def __str__(self):
        return self.seller.username
