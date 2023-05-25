from django.db import models

# Create your models here.
class Movies(models.Model):
    movie_title = models.CharField(max_length = 250)
    rating = models.FloatField(null=True, blank=True, default=None)
    movie_poster = models.TextField(blank = True, null = True)
    movie_source = models.CharField(max_length = 255)
    created_by = models.IntegerField(null = True)
    created_date = models.DateTimeField(null = True)

    def __str__(self):
        return self.movie_title
