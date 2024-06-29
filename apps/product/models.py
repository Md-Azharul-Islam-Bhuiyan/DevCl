from django.db import models
from django.utils import timezone, text
from apps.account.models import SellerProfile


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    class TAX_TYPE(models.TextChoices):
        SHIPPING = 'SHIPPING', 'Shipping'
        VAT = 'VAT', 'Vat'

    class STATUS_TYPE(models.TextChoices):
        STOCK = "STOCK", 'Stock'
        UNAVAILABLE = "UNAVAILABLE", "Unavailable"
        UPCOMMING = "UPCOMMING", "Upcomming"

    product_name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.CharField(max_length=30)
    sku = models.CharField(max_length=30)
    minimum_quantity = models.IntegerField(default=1)
    quantity = models.IntegerField(default=1)
    description = models.TextField()
    tax = models.CharField(
        max_length=20, choices=TAX_TYPE.choices, default=TAX_TYPE.VAT
    )
    discount = models.FloatField(default=0.00)
    price = models.FloatField()
    status = models.CharField(
        max_length=20, choices=STATUS_TYPE.choices, default=STATUS_TYPE.STOCK
    )
    product_image = models.ImageField(upload_to='product/images/', default=None)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name