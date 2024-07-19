from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError


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
        self.slug = slugify(self.name)
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
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=256, unique=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=1)
    status = models.PositiveIntegerField(choices= STATUS_CHOICES, default=1)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if Product.objects.exclude(id=self.id).filter(slug=slug).exists():
            self.slug = f"{slug}-{self.id}"
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
    
