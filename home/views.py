from typing import Any, Dict
from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import User,Customer
from .models import Wishlist,WishlistItems
from django.contrib.auth.models import User
from django.contrib import messages
from customers.models import Cart
from django.views.generic import CreateView,ListView, DetailView
from django.contrib.auth import login,authenticate, get_user_model,logout
from vendors.models import Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

def home(request): 
        return redirect('homepage')

def about(request):
    return render(request, 'home/about.html')

def sign_in(request): 
    return render(request, 'home/sign_in.html')

def sign_up(request): 
    return render(request, 'home/sign_up.html')

def add_to_wishlist(request,id):
        item=Item.objects.get(id=id)
        user=request.user
        wishlist, _ = Wishlist.objects.get_or_create(user = user)
        f=0
        for obj in WishlistItems.objects.filter(wishlist=wishlist):
            if obj.item == item:
                f=1
        if f==0:
            wishlist_item=WishlistItems.objects.create(wishlist=wishlist, item=item,)
            wishlist_item.save()
            messages.success(request, f'Your item has been added to wishlist!')
        else:
            messages.info(request, f'Item is already in your wishlist!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_wishlist(request,wishlist_item_id):
        try:
            wishlist_item = WishlistItems.objects.get(id= wishlist_item_id)
            wishlist_item.delete()
        except Exception as e:
            print(e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def wishlist(request):
        if Cart.objects.filter(user= request.user,is_paid=False).exists():
                obj=Cart.objects.get(user= request.user,is_paid=False)
                count=obj.get_cart_count
        else: 
                count=0
        if Wishlist.objects.filter(user= request.user).exists():
            if WishlistItems.objects.filter(wishlist= Wishlist.objects.get(user= request.user)).exists():
                wishlist_obj= Wishlist.objects.filter(user= request.user)
                w_obj=  Wishlist.objects.get(user= request.user)
                l=WishlistItems.objects.all()
                wishlistitems=[]
                for product in l:
                    for p in wishlist_obj:
                        if product.wishlist== p:
                            if product.item.units_available == 0 :
                                p.is_outofstock= True
                                p.save()
                            if p.is_outofstock == True and product.item.units_available != 0 :
                                p.is_outofstock= False
                                p.save()
                                template= render_to_string('home/customer_email.html',{'product': product , 'wishlist_obj': w_obj})
                                email_customer= EmailMessage('Shopmart.in purchase made',template,settings.EMAIL_HOST_USER,[request.user.email])
                                email_customer.fail_silently = False
                                email_customer.send()

                            wishlistitems.append(product)
                context= {'wishlistitems': wishlistitems , 'wishlist_obj': w_obj,'count': count}
                return render(request,'home/wishlist.html', context)
            else:
                messages.info(request,f"Your Wishlist is Empty.")
                return render(request,'home/wishlist.html', {'wishlistitems':'', 'wishlist_obj':'','count':count })
        else:
            messages.info(request,f"Your Wishlist is Empty.")
            return render(request,'home/wishlist.html', {'wishlistitems':'', 'wishlist_obj':'','count':count })
