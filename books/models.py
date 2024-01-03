from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField()
    slug=models.SlugField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.category_name
    
class Book(models.Model):
    book_image = models.FileField(upload_to='books/media/uploads/', blank=True, null=True)
    book_name = models.CharField(max_length=100)
    book_price=models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    book_quantity=models.IntegerField(blank=True, null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.book_name