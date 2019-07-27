from django.db import models
from users.models import CustomUser
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    price=models.IntegerField(null=False)

    def __str__(self):
        return f'{self.title}-> ₹{self.price}'
    def get_absolute_url(self):
        return reverse('category')


class Order(models.Model):
    MY_CHOICES = (
    ('Placed', 'Placed'),
    ('Processing', 'Processing'),
    ('Rejected','Rejected'),
    ('Complete','Complete'),
)
    customer=models.ForeignKey(CustomUser,on_delete=models.CASCADE) 
    type=models.ForeignKey(Category,on_delete=models.CASCADE)
    trans_id=models.CharField(max_length=100,null=False)
    character_id=models.CharField(max_length=100,null=False) 
    password=models.CharField(max_length=100,null=False)    
    status= models.CharField(max_length=10,choices=MY_CHOICES,default='Placed')
    order_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.customer.email

