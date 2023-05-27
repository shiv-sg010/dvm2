from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Vendor)
admin.site.register(models.Customer)
admin.site.register(models.Profile)