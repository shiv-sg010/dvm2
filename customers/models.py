from django.db import models
from accounts.models import User
from vendors.models import Item
from django.contrib.auth import get_user_model
from django.utils import timezone

User=get_user_model()

class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid= models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price=[]
        for cart_item in cart_items:
            price.append(cart_item.item.price*cart_item.quantity)
        return sum(price)
    
    def get_cart_count(self):
        cart_items = self.cart_items.all()
        count=0
        for items in cart_items:
            count+= items.quantity
        return count
                
    
class CartItems(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item=models.ForeignKey(Item, on_delete=models.SET_NULL,null=True ,blank= True)
    quantity= models.PositiveIntegerField(default=1)

    def get_item_price(self):
        price= (self.item.price)*(self.quantity)
        return (price)
    
class MyOrder(models.Model):
    customer= models.ForeignKey(User, on_delete=models.CASCADE)
    vendor=models.TextField()
    image= models.ImageField(default='default.jpg', upload_to='item_pics')
    title= models.CharField(max_length=100)
    description= models.TextField()
    price=models.FloatField()
    quantity=models.PositiveIntegerField(default=1)
    date_purchased= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer.username

    def get_price(self):
        price= (self.price)*(self.quantity)
        return (price)

