from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('vendor_register/',views.register.as_view(),name='vendor-register'),
    path('vendor_login/',views.login_view,name='vendor-login'),
    path('vendor_logout/', auth_views.LogoutView.as_view(template_name='vendors/logout.html'),name='vendor-logout'),
    path('venor_profile/', views.profile, name='vendor-profile'),
    path('vendor/<str:username>', views.VendorItemListView.as_view(), name='dashboard'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', views.ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
    path('v_role/', views.v_role, name='v_role'),
    path('v_check/', views.v_check, name='v_check'),
    path('order/', views.PurchaseView, name='orders'),
    path('export/excel/', views.export_orders_xls, name='order_excel')
]