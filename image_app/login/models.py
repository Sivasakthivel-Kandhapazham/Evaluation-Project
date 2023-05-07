from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    email_id = models.CharField(max_length = 255, unique =  True)
    password = models.CharField(max_length = 50)
    mobile_no = models.IntegerField(null = True)
    gender = models.IntegerField()

    def __str__(self):
        return self.firstname
