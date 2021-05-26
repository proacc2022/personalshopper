from django.db import models

# Create your models here.
from mptt.fields import TreeForeignKey
from django.urls import reverse
from mptt.models import MPTTModel


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.category_name

    class MPTTMeta:
        order_insertion_by = ['category_name']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.category_name]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.category_name)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # many to one relation with Category
    product_name = models.CharField(max_length=300)
    product_keywords = models.CharField(max_length=255)
    product_description = models.TextField(max_length=600)
    product_image = models.ImageField(upload_to='images/', null=False)
    product_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    product_brand = models.CharField(max_length=200)
    product_stock = models.IntegerField(default=3)
    product_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images/')

    def __int__(self):
        return self.product
