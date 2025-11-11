from django.db import models
from django.contrib.auth.models import AbstractUser

 
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username


# 🌿 Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 🌍 Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    eco_rating = models.IntegerField(default=5)

    def __str__(self):
        return self.name


# 📝 Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.CharField(max_length=100, default='EcoCart Team')
    date = models.DateField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title


# 🛒 Cart Model
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.user.username}"

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='wishlist_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"

