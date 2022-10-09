from django.db import models

from ads.models.location import Location


class User(models.Model):
    ROLES = [
        ("admin", "администратор"),
        ("member", "пользователь"),
        ("moderator", "модератор"),
    ]

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=150, null=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=10, choices=ROLES, default="member")
    age = models.SmallIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
