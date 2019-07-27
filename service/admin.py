from django.contrib import admin

# Register your models here.
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','type','trans_id','status','character_id','password','order_date')
    list_filter = ('type', 'status','order_date')




admin.site.register(Category)
admin.site.register(Order,OrderAdmin)
