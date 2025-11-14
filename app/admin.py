from django.contrib import admin
from .models import Blog,Product,Order,OrderItem,CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)


