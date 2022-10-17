from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
  regex=r'^\+?1?\d{9,15}$',
  message=
  "Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed."
)


# Create your models here.
class CustomUser(AbstractUser):
  phone = models.CharField(validators=[phone_regex],
                           unique=True,
                           max_length=15)
  type = models.CharField(max_length=20, blank=True, null=True)
  org = models.ForeignKey('Organization',
                          on_delete=models.CASCADE,
                          blank=True,
                          null=True)
  is_active = models.BooleanField(
        default=True,
    )
  def save(self, *args, **kwargs):
    if not self.username:
      self.username=self.phone
    if self.is_superuser:
      self.is_active=True
    super(CustomUser, self).save(*args, **kwargs)

class Organization(models.Model):
  name = models.CharField(max_length=200)
  primary_name = models.CharField(max_length=200)
  primary_title = models.CharField(max_length=200)
  phone = models.CharField(validators=[phone_regex], max_length=15)
  email = models.EmailField(blank=True, unique=True)
  owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  address = models.TextField(default="")
  city = models.CharField(max_length=200)
  state = models.CharField(max_length=200)
  zip = models.CharField(max_length=200)
  note = models.TextField(default="")


class Product(models.Model):
  name = models.CharField(max_length=200)
  image = models.FileField(upload_to='uploads/')
  organization = models.ManyToManyField(Organization)
  test_for = models.TextField(default="")
  sku = models.CharField(max_length=230)


class Report(models.Model):
  user = models.ForeignKey(CustomUser,
                           on_delete=models.CASCADE,
                           related_name='customuser')
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  administrator = models.ForeignKey(CustomUser,
                                    on_delete=models.CASCADE,
                                    related_name='admin_customuser')
  test_result = models.CharField(max_length=230)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  datetime = models.DateTimeField()
