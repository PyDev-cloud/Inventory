from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(category)
admin.site.register(SubCategory)
admin.site.register(product)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Purchase)