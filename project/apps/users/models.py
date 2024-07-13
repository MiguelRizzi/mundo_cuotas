from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return f'img/users/{instance.user.username}/{filename}'

    
class Avatar(models.Model):
    user = models.OneToOneField(User, blank=False, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path) 

    def __str__(self):
        return self.user.username
    

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now=True)
    is_read = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name