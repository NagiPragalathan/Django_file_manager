from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class ImageEditor(models.Model):
    question = RichTextUploadingField()

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

class McqQuestionBase(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # Question details
    question = models.TextField()
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    category = models.CharField(max_length=255)
    question_type = models.CharField(max_length=50)  # You might want to limit the choices here
    # Options and correct answer
    options = models.JSONField()  # Assuming options will be stored as a JSON array
    correct_answer = models.CharField(max_length=255)
    instructions = models.TextField()
    Para_quest = models.TextField(null=True, blank=True)
    copy_qust_path =  models.TextField()
    quest_id = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=400)
    # Timestamps
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.question}"
    def save(self, *args, **kwargs):
            # Trim and remove duplicates from the comma-separated path
            if self.copy_qust_path:
                paths = [path.strip() for path in self.copy_qust_path.split(',')]
                paths = list(set(paths))  # Remove duplicates
                self.copy_qust_path = ', '.join(paths)
            super().save(*args, **kwargs)