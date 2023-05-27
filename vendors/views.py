from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import User, Vendor
from customers.models import MyOrder
from .models import Item
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm,LoginForm,VendorUpdateForm,ProfileUpdateForm
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate, get_user_model,logout
from django.contrib.auth.mixins import UserPassesTestMixin
import xlwt
from django.http import HttpResponse


User=get_user_model()

class register(CreateView):
    model= User
    form_class = UserRegisterForm
    template_name= 'vendors/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type']= 'vendor'
        return super().get_context_data(**kwargs)
    
    def form_valid(self,form):
            user=form.save()
            messages.success(self.request, f'Your account has now been created! You are now logged in.')
            login(self.request,user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard',user.username)
    

def login_view(request):
    form= LoginForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user= authenticate(username= username, password=password)
            if user is not None and user.is_vendor:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dashboard', user.username)
            else:
                messages.error(request, f'Invalid credentials! Try Again.')
        else:
            messages.error(request,f'Error validating form!')
    return render(request,'vendors/login.html',{'form': form })

@login_required
def profile(request):
    if request.method=='POST':
        u_form=VendorUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            if request.POST!= request.user and request.POST!=request.user.profile:
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('vendor-profile')
    else:
        u_form=VendorUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request,'vendors/profile.html',context)


@login_required
def dashboard(request):
    return render(request, 'vendors/home.html')


class VendorItemListView(ListView):
    model= Item
    template_name= 'vendors/home.html'
    context_object_name= 'items'
    paginate_by =3 
    
    def get_queryset(self):
        user= get_object_or_404(User , username=self.kwargs.get('username'))
        return Item.objects.filter(vendor=user).order_by('-quantity_purchased')

class ItemDetailView(UserPassesTestMixin,DetailView):
    model= Item
    template_name='vendors/details.html'

    def test_func(self):
        item=self.get_object()
        if self.request.user== item.vendor:
            return True
        return False

class ItemCreateView(CreateView):
    model= Item
    template_name= 'vendors/new.html'
    fields =['image','title','description','units','price']

    def form_valid(self, form):
        form.instance.vendor= self.request.user
        messages.success(self.request, f'Your item has been added.')
        return super().form_valid(form)
    
class ItemUpdateView(UserPassesTestMixin,UpdateView):
    model= Item
    template_name= 'vendors/update.html'
    fields =['image','title','description','units','price']

    def form_valid(self, form):
        form.instance.vendor= self.request.user
        messages.success(self.request, f'Your item has been updated.')
        return super().form_valid(form)
    
    def test_func(self):
        item=self.get_object()
        if self.request.user== item.vendor:
            return True
        return False
    
class ItemDeleteView(UserPassesTestMixin,DeleteView):
    model= Item
    template_name='vendors/delete.html'
    
    def get_success_url(self):
        messages.success(self.request, f'Your item is successfully deleted.')
        return reverse('dashboard',kwargs={'username':self.request.user.username})

    def test_func(self):
        item=self.get_object()
        if self.request.user== item.vendor:
            return True
        return False

def v_role(request):
    user=request.user
    if user.is_customer == False and user.is_vendor == False:
        user.is_vendor= True
        user.save()
        vendor= Vendor.objects.create(user=user,email=user.email)
        vendor.save()
        messages.success(request, f'Your account has now been created!')
        return redirect('dashboard',user.username)
    else:
        logout(request)
        messages.error(request,f'User Already exists!Try to Log in.')
        return redirect('sign_in')


def v_check(request):
    user=request.user
    if user.is_customer == False and user.is_vendor == False: 
        logout(request)
        messages.info(request, f'You need to register first.')
        return redirect('sign_up')
    elif user.is_vendor == True:
        return redirect('dashboard', user.username)
    else:
        logout(request)
        messages.error(request,f'You are not authorized as Vendor! Log in Again.')
        return redirect('vendor-login')
    
@login_required
def PurchaseView(request):
    user=request.user
    if MyOrder.objects.filter(vendor=user).exists():
        order= MyOrder.objects.filter(vendor=user)
        return render(request,'vendors/order.html',{'order':order})
    else:
        messages.info(request,f"You have no current order.")
        return render(request,'vendors/order.html',{'order':''})
    


def export_orders_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Orders Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['vendor','title', 'quantity' , 'price' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = MyOrder.objects.filter(vendor= request.user).values_list( 'vendor','title', 'quantity' , 'price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response