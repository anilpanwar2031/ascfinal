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
  options = (
    ("OA", "Organization Admin"),
    ("SA", "Super Admin"),
    ("NU", "Normal User"),
  )
  type = models.CharField(choices=options, max_length=20, default="NU")
  org = models.ForeignKey('Organization',
                          on_delete=models.CASCADE,
                          blank=True,
                          null=True)
  is_active = models.BooleanField(default=False)

  def __str__(self):
    return self.first_name

  def save(self, *args, **kwargs):
    if not self.username:
      self.username = self.phone
    if self.is_superuser:
      self.is_active = True
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

  def __str__(self):
    return self.name


class Product(models.Model):
  GS1_Company_Prefix = models.CharField(max_length=255, blank=True, null=True)
  GTIN = models.CharField(max_length=255, blank=True, null=True)
  GTIN_8 = models.CharField(max_length=255, blank=True, null=True)
  GTIN_12_UPC = models.CharField(max_length=255, blank=True, null=True)
  GTIN_13_EAN = models.CharField(max_length=255, blank=True, null=True)
  Brand_Name = models.CharField(max_length=255, blank=True, null=True)
  Brand_1_Language = models.CharField(max_length=255, blank=True, null=True)
  Product_Description = models.CharField(max_length=255, blank=True, null=True)
  Desc_1_Language = models.CharField(max_length=255, blank=True, null=True)
  Product_Industry = models.CharField(max_length=255, blank=True, null=True)
  Packaging_Level = models.CharField(max_length=255, blank=True, null=True)
  Is_Variable = models.BooleanField(blank=True)
  Is_Purchasable = models.BooleanField(blank=True)
  Status_Label = models.CharField(max_length=255, blank=True, null=True)
  Height = models.CharField(max_length=255, blank=True, null=True)
  Width = models.CharField(max_length=255, blank=True, null=True)
  Depth = models.CharField(max_length=255, blank=True, null=True)
  Dimension_Measure = models.CharField(max_length=255, blank=True, null=True)
  Gross_Weight = models.CharField(max_length=255, blank=True, null=True)
  Net_Weight = models.CharField(max_length=255, blank=True, null=True)
  Weight_Measure = models.CharField(max_length=255, blank=True, null=True)
  SKU = models.CharField(max_length=255, blank=True, null=True)
  Sub_brand_Name = models.CharField(max_length=255, blank=True, null=True)
  Product_Description_Short = models.CharField(max_length=255,
                                               blank=True,
                                               null=True)
  Label_Description = models.CharField(max_length=255, blank=True, null=True)
  Net_Content_1_Count = models.CharField(max_length=255, blank=True, null=True)
  Net_Content_1_Unit_of_Measure = models.CharField(max_length=255,
                                                   blank=True,
                                                   null=True)
  Net_Content_2_Count = models.CharField(max_length=255, blank=True, null=True)
  Net_Content_2_Unit_of_Measure = models.CharField(max_length=255,
                                                   blank=True,
                                                   null=True)
  Net_Content_3_Count = models.CharField(max_length=255, blank=True, null=True)
  Net_Content_3_Unit_of_Measure = models.CharField(max_length=255,
                                                   blank=True,
                                                   null=True)
  Brand_Name_2 = models.CharField(max_length=255, blank=True, null=True)
  Brand_2_Language = models.CharField(max_length=255, blank=True, null=True)
  Description_2 = models.CharField(max_length=255, blank=True, null=True)
  Desc_2_Language = models.CharField(max_length=255, blank=True, null=True)
  Global_Product_Classification = models.CharField(max_length=255,
                                                   blank=True,
                                                   null=True)
  Image_URL = models.FileField(upload_to='media/uploads/', null=True)
  Image_URL_Validation = models.CharField(max_length=255,
                                          blank=True,
                                          null=True)
  Target_Markets = models.CharField(max_length=255, blank=True, null=True)
  Last_Modified_Date = models.DateField(blank=True, null=True)
  organization = models.ManyToManyField(Organization, null=True)
  test_for = models.TextField(null=True, blank=True)


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
