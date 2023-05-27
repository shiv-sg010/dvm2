from django.db import models
from accounts.models import User
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PIL import Image
from django.urls import reverse

User=get_user_model()
class Item(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default.jpg', upload_to='item_pics')
    title= models.CharField(max_length=100)
    description= models.TextField()
    units= models.IntegerField()
    price=models.FloatField()
    quantity_purchased= models.IntegerField(default=0)
    units_available= models.PositiveIntegerField(default= units)

    def save(self, *args,**kwargs):
        self.units_available= self.units-self.quantity_purchased
        super( Item, self).save(*args,**kwargs)

        img= Image.open(self.image.path)

        if img.mode != 'RGB':
            img=img.convert('RGB')

        if img.height>300 or img.width>300:
            output_size =(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('dashboard', kwargs={'username':self.vendor})
    
    def most_buyed(self):
        items= Item.objects.all()
        max=0
        for i in items:
            if max < i.quantity_purchased:
                max= i.quantity_purchased
        return max

    
