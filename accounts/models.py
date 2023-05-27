from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# redifinig users
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    address = models.TextField(null=True)
    email = models.EmailField(null=True)
    amount=models.FloatField(default=0.0)


# vendor models
class Vendor(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.user.username


# customer models
class Customer(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField(null=True)
    email = models.EmailField(null=True)
    amount= models.FloatField(null=True, default=0.0)

    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default_profile.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args,**kwargs):
        super( Profile, self).save(*args,**kwargs)

        img= Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size =(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


