from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    code = models.CharField(max_length=6,null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')



    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')

    company_name = models.CharField(max_length=255)
    company_reg_number = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    company_website = models.URLField(blank=True, null=True)
    business_address = models.TextField()

    company_certificate = models.FileField(upload_to='documents/company_certificates/')
    owner_id = models.FileField(upload_to='documents/owner_ids/')
    company_logo = models.ImageField(upload_to='images/company_logos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"