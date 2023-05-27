from django.contrib import admin
from .models import Cart, CartItems, MyOrder
from import_export.admin import ImportExportModelAdmin

admin.site.register(Cart)
admin.site.register(CartItems)


class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display= ('customer','vendor','title','description','price','quantity','date_purchased')

admin.site.register(MyOrder,OrderAdmin)
