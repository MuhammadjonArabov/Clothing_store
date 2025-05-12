from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError(_("The phone must be set"))
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be assigned to is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must be assigned to is_superuser=True."))
        return self.create_user(phone, password, **extra_fields)

    def normalize_phone(self, phone):
        return phone

phone_validator = RegexValidator(regex=r"^\+998\d{9}$", message="Phone number must be in the format +998991234567")

class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    username = None

    class RoleType(models.TextChoices):
        ADMIN = "admin", "Admin"
        SELLER = "seller", "Seller"
        CUSTOMER = "customer", "Customer"

    class GenderType(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    phone = models.CharField(validators=[phone_validator], unique=True)
    role = models.CharField(max_length=10, choices=RoleType.choices, default=RoleType.CUSTOMER)
    gender = models.CharField(max_length=10, choices=GenderType.choices, default=GenderType.MALE)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now_add=True)
   

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone
    