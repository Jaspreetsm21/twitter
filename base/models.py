from django.db import models

# Create your models here.
class Twitter_Model(models.Model):
    name = models.CharField(max_length=10000)
    def __str__(self):
        return self.name