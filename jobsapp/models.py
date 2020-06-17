from django.db import models
from django.utils import timezone

from accounts.models import User

JOB_TYPE = (
    ('1', "Робота"),
    ('2', "Випробування"),
    ('3', "Стажування"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Практика'
 

    def __str__(self):
        return self.title


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = 'Заявники'
    def __str__(self):
        return self.user.get_full_name()

class About(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    messages = models.TextField()
    class Meta:
        verbose_name_plural = 'Повідомлення'
    def __str__(self):
        return self.name