from django.db import models

# Create your models here.
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    price = models.IntegerField(default=0)
    stripe_product_id = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

