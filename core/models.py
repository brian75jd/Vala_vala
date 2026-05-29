from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media')
    badge = models.CharField(max_length=50,null=True,blank=True)
    desc = models.CharField(max_length=350)
    date_created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name
