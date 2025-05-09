from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The phone must be set")
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
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        return self.create_user(phone, password, **extra_fields)
    
    
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
    role = models.CharField(max_length=5, choices=RoleType.choices, default=RoleType.CUSTOMER)
    gender = models.CharField(max_length=5, choices=GenderType.choices, default=GenderType.MALE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now_add=True)
    
    # Social authentication fields
    google_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    facebook_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    social_email = models.EmailField(null=True, blank=True)
    social_name = models.CharField(max_length=255, null=True, blank=True)
    social_avatar = models.URLField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone
    