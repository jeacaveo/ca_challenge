from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Review(models.Model):
    RATINGS = (("1", "1"),
               ("2", "2"),
               ("3", "3"),
               ("4", "4"),
               ("5", "5"),
               )

    rating = models.CharField(max_length=2, choices=RATINGS)
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=10000)
    ip_address = models.CharField(max_length=20)
    submission_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company)
    reviewer = models.ForeignKey(User)

    class Meta:
        ordering = ["-submission_date"]
