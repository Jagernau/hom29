from django.db import models

from users.models import User
from ads.models.category import Category


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=2000)
    is_published = models.BooleanField(default=None)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
