from django.db import models


# Create your models here.
class Category(models.Model):
    category_type = models.CharField(max_length=255)
    is_active = models.BooleanField()


class ImageGallery(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    category_type = models.ForeignKey(Category, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    image = models.ImageField(upload_to = 'images/')
    created_by = models.IntegerField(null = True)
    created_date = models.DateTimeField(null = True)

    def __str__(self):
        return self.title
