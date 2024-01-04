from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User


class OTPVerification(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    otp_key = models.CharField(max_length=6)  # Adjust the max_length as needed
    updated_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"OTPVerification(id={self.id}, otp_key={self.otp_key}, updated_time={self.updated_time})"
    
class PathManager(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=400)  # Adjust max_length as needed
    file = models.FileField(upload_to='Files/')  # Adjust upload_to as needed
    category = models.CharField(max_length=50)  # Adjust max_length as needed
    title = models.CharField(max_length=255)  # Adjust max_length as needed
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.user_id.username}'
    
class FolderManager(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    FolderName = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    path = models.CharField(max_length=400)
    updated_date = models.DateTimeField(auto_now=True)
