from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        "self",
        related_name="subcategories",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=256, unique=True)
    
    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError('No se permite anidar mas de dos categorias')

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if Category.objects.exclude(id=self.id).filter(slug=slug).exists():
            self.slug = f"{slug}-{self.parent.id}"
        else:
            self.slug = slug
        super().save(*args, **kwargs)
        return

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.slug)])
    
    
class Product(models.Model):
    TYPE_CHOICES = ( 
        (1, "Regular"),
        (2, "Oferta"),
        (3, "Destacado")
    )
    STATUS_CHOICES = (
        (1, "No publicado"),
        (2, "Publicado")
    )
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_cash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_12_weeks = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_6_fortnights= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_3_months = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=256, unique=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=1)
    status = models.PositiveIntegerField(choices= STATUS_CHOICES, default=1)

    def save(self, *args, **kwargs):
        self.price_12_weeks = None 
        self.price_6_fortnights = None
        self.price_3_months = None

        if self.price_cash and not self.category.name == "Motos":
            
            if self.price_cash <= 99999:
                financed_price = self.price_cash + (self.price_cash * Decimal('1.2'))
            
                self.price_12_weeks = financed_price / Decimal('12')
                self.price_6_fortnights = financed_price / Decimal('6')
                self.price_3_months = financed_price / Decimal('3')
            
            elif self.price_cash > 99999 and self.price_cost:
                financed_price = self.price_cost + (self.price_cost * Decimal('1.2'))
            
                self.price_12_weeks = financed_price / Decimal('12')
                self.price_6_fortnights = financed_price / Decimal('6')
                self.price_3_months = financed_price / Decimal('3')
            

        slug = slugify(self.name)
        if Product.objects.exclude(id=self.id).filter(slug=slug).exists():
            self.slug = f"{slug}-{self.category.id}"
        else:
            self.slug = slug
        super().save(*args, **kwargs)
        return

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[str(self.slug)])
    
    
class File(models.Model):
    file= models.FileField(upload_to="productos/", null=True)
    product= models.ForeignKey(Product, related_name="files", on_delete=models.CASCADE)
    def __str__(self):
        return self.file.name
    
