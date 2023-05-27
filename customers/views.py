from typing import Any, Dict
from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import User,Customer
from .models import Cart,CartItems,MyOrder
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm, CustomerUpdateForm,ProfileUpdateForm
from django.views.generic import CreateView,ListView, DetailView
from django.contrib.auth import login,authenticate, get_user_model,logout
from vendors.models import Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

User=get_user_model()

class register(CreateView):
    model= User
    form_class = UserRegisterForm
    template_name= 'customers/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type']= 'customer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self,form):
            user=form.save()
            messages.success(self.request, f'Your account has now been created! You are now logged in.')
            login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
            obj=Cart.objects.get(user= self.request.user,is_paid=False)
            return redirect('homepage',{'obj': obj})
    

def login_view(request):
    form= LoginForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user= authenticate(username= username, password=password)
            if user is not None and user.is_customer:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('homepage')
            else:
                messages.error(request, f'Invalid credentials! Try Again.')
        else:
            messages.error(request,f'Error validating form!')
    return render(request,'customers/login.html',{'form': form })

class ItemListView(ListView):
    model= Item
    template_name= 'customers/home.html'
    context_object_name= 'items'
    ordering='-quantity_purchased'
    paginate_by =3

    def get_context_data(self, **kwargs):
        context= super(ItemListView,self).get_context_data(**kwargs)
        if Cart.objects.filter(user= self.request.user.id,is_paid=False).exists():
                obj=Cart.objects.get(user= self.request.user,is_paid=False)
                count=obj.get_cart_count
        else: 
            count=0
        context['count']= count
        return context



class ItemDetailView(DetailView):
    model= Item
    template_name='customers/details.html'

    def get_context_data(self, **kwargs):
        context= super(ItemDetailView,self).get_context_data(**kwargs)
        if Cart.objects.filter(user= self.request.user.id,is_paid=False).exists():
                    obj=Cart.objects.get(user= self.request.user,is_paid=False)
                    count=obj.get_cart_count
        else: 
            count=0
        context['count']= count
        return context
    
    


@login_required
def profile(request):
    if request.method=='POST':
        u_form=CustomerUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            if request.POST!= request.user and request.POST!=request.user.profile:
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('customer-profile')
    else:
        u_form=CustomerUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)

    if Cart.objects.filter(user= request.user,is_paid=False).exists():
                    obj=Cart.objects.get(user= request.user,is_paid=False)
                    count=obj.get_cart_count
    else: 
            count=0

    context={
        'u_form':u_form,
        'p_form':p_form,
        'count': count,
    }
    return render(request,'customers/profile.html',context)

class UserItemListView(ListView):
    model= Item
    template_name= 'customers/items.html'
    context_object_name= 'items'
    paginate_by =3 

    def get_context_data(self, **kwargs):
        context= super(UserItemListView,self).get_context_data(**kwargs)
        if Cart.objects.filter(user= self.request.user,is_paid=False).exists():
                    obj=Cart.objects.get(user= self.request.user,is_paid=False)
                    count=obj.get_cart_count
        else: 
            count=0
        context['count']= count
        return context

    def get_queryset(self):
        user= get_object_or_404(User , username=self.kwargs.get('username'))
        return Item.objects.filter(vendor=user).order_by('-quantity_purchased')

def add_to_cart(request,id):
    item=Item.objects.get(id=id)
    user=request.user
    cart, _ = Cart.objects.get_or_create(user = user, is_paid = False)
    f=0
    for obj in CartItems.objects.filter(cart=cart):
        if obj.item == item:
            f=1
    if f==0:
        cart_item=CartItems.objects.create(cart= cart, item=item,)
        cart_item.save()
        messages.success(request, f'Your item has been added to cart!')
    else:
        cart_item=CartItems.objects.get(cart=cart,item=item)
        cart_item.quantity+=1
        cart_item.save()
        messages.success(request, f'Your cart has been updated!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request,cart_item_id):
    try:
        cart_item = CartItems.objects.get(id= cart_item_id)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def cart(request):
    if Cart.objects.filter(user= request.user, is_paid = False).exists():
        if CartItems.objects.filter(cart= Cart.objects.get(user= request.user, is_paid=False)).exists():
            cart_obj= Cart.objects.filter(user= request.user,is_paid=False)
            l=CartItems.objects.all()
            units=list(range(1,11))
            cartitems=[]
            count=0
            for product in l:
                for p in cart_obj:
                    if product.cart== p:
                        count+= product.quantity
                        cartitems.append(product)
            context= {'cartitems': cartitems , 'cart_obj': cart_obj, 'units':units, 'count': count}
            return render(request,'customers/cart.html', context)
        else:
            messages.info(request,f"Your Cart is Empty.")
            return render(request,'customers/cart.html', {'cartitems':'', 'cart_obj':'', 'units':'','count':0 })
    else:
        messages.info(request,f"Your Cart is Empty.")
        return render(request,'customers/cart.html', {'cartitems':'', 'cart_obj':'', 'units':'', 'count':0 })
    
def c_role(request):
    user=request.user
    if user.is_customer == False and user.is_vendor == False:
        user.is_customer= True
        user.save()
        customer= Customer.objects.create(user=user,email=user.email)
        customer.save()
        messages.success(request, f'Your account has now been created!')
        return redirect('homepage')
    else:
        logout(request)
        messages.error(request,f'User Already exists!Try to Log in.')
        return redirect('sign_in')


def c_check(request):
    user=request.user
    if user.is_customer == False and user.is_vendor == False: 
        logout(request)
        messages.info(request, f'You need to register first.')
        return redirect('sign_up')
    elif user.is_customer == True:
        return redirect('homepage')
    else:
        logout(request)
        messages.error(request,f'You are not registered as Customer!Log in Again.')
        return redirect('customer-login')

@login_required
def QuantityUpdate(request,id):
    if request.method=='POST':
        quantity = float(request.POST.get("quantity_select"))
        quantity= int(quantity)
        item=Item.objects.get(id=id)
        cart_obj = Cart.objects.get(user= request.user,is_paid=False)
        cart_item=CartItems.objects.get(cart=cart_obj,item=item)
        cart_item.quantity=quantity
        cart_item.save()
        messages.success(request, f'Your cart has been updated!')
    return redirect('cart')

@login_required
def purchase_page(request):
    cart_obj= Cart.objects.filter(user= request.user,is_paid=False)
    l=CartItems.objects.all()
    cartitems=[]
    count=0
    for product in l:
        for p in cart_obj:
            if product.cart== p:
                count+=product.quantity
                cartitems.append(product)
    context= {'cartitems': cartitems , 'cart_obj': cart_obj, 'count':count ,'obj': Cart.objects.get(user= request.user, is_paid= False)}
    return render(request,'customers/purchase.html', context)

@login_required
def success(request):
    cart_obj= Cart.objects.filter(user= request.user,is_paid=False)
    obj=Cart.objects.get(user= request.user,is_paid=False)
    price=obj.get_cart_total()
    if request.user.amount >= price:
        l=CartItems.objects.all()
        cartitems=[]
        for product in l:
            for p in cart_obj:
                if product.cart== p:
                    cartitems.append(product)
                    template1= render_to_string('customers/vendor_email.html',{'product': product , 'obj': obj})
                    email_vendor= EmailMessage('Shopmart.in purchase made',template1,settings.EMAIL_HOST_USER,[product.item.vendor.email])
                    email_vendor.fail_silently = False
                    email_vendor.send()
                    product.item.quantity_purchased+= product.quantity
                    product.item.save()
                    order=MyOrder.objects.create(customer=request.user,vendor=product.item.vendor.username,image=product.item.image,title=product.item.title,description=product.item.description,price=product.item.price,quantity=product.quantity)
                    order.save()

        template= render_to_string('customers/customer_email.html', {'obj': obj})
        email_customer= EmailMessage('Your Shopmart.in order',template,settings.EMAIL_HOST_USER,[request.user.email])
        email_customer.fail_silently = False
        email_customer.send()

        obj.is_paid= True
        obj.save()
        request.user.amount -= price
        request.user.save()

    else:
        messages.error(request,f'Insufficient Balance in Account! Update your Account.')
        return redirect('purchase-page')

    return render(request,'customers/success.html',{'count':0 })

@login_required
def OrderView(request):
    user=request.user
    if Cart.objects.filter(user= request.user,is_paid=False).exists():
            obj=Cart.objects.get(user= request.user,is_paid=False)
            count=obj.get_cart_count
    else: 
            count=0
    if MyOrder.objects.filter(customer=user).exists():
        order= MyOrder.objects.filter(customer=user)
        return render(request,'customers/order.html',{'order':order, 'count': count})
    else:
        messages.info(request,f"You have no previous order.")
        return render(request,'customers/order.html',{'order':'','count':count})
    
