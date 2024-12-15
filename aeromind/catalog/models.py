from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/')
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='ratings')  # Reference to the product
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')  # User who submitted the rating
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating between 1 and 5 stars
    review = models.TextField(blank=True, null=True)  # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)  # Time when the rating was submitted

    def __str__(self):
        return f'{self.user.username} rated {self.product.name} {self.rating} stars'
