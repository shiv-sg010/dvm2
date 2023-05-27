from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('customer_register/',views.register.as_view(),name='customer-register'),
    path('customer_login/', views.login_view,name='customer-login'),
    path('customer_logout/', auth_views.LogoutView.as_view(template_name='customers/logout.html'),name='customer-logout'),
    path('homepage/', views.ItemListView.as_view(), name='homepage'),
    path('customer_profile/', views.profile, name='customer-profile'),
    path('user/<str:username>/', views.UserItemListView.as_view(), name='user-items'),
    path('item_view/<int:pk>/', views.ItemDetailView.as_view(), name='item-view'),
    path('cart/', views.cart, name='cart'),  
    path('add-to-cart/<id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-cart/<cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('c_role/', views.c_role, name='c_role'),
    path('c_check/', views.c_check, name='c_check'),
    path('quanity/<id>/', views.QuantityUpdate, name= 'quantity-update'),
    path('purchase/',views.purchase_page, name='purchase-page'),
    path('success/', views.success , name= 'success'),
    path('myorder/', views.OrderView, name='Myorder')
]