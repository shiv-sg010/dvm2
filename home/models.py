from django.db import models
from accounts.models import User
from vendors.models import Item
from django.contrib.auth import get_user_model
from django.utils import timezone

User=get_user_model()

class Wishlist(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    is_outofstock= models.BooleanField(default=False)

                
    
class WishlistItems(models.Model):
    wishlist=models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    item=models.ForeignKey(Item, on_delete=models.SET_NULL,null=True ,blank= True)
