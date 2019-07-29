from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from service.models import Order
from users.models import CustomUser as user 
from . forms import *
from datetime import date
from django.views.generic import (
        ListView,                  
)

def home(request):
    try:
        image=user.objects.filter(is_staff=True,is_superuser=False).first()
        msg=image.profile.offer
    except:
        if request.user.is_authenticated and request.user.is_staff == True:
            msg="Staff user profile not is not created. Contact owner"           
    
    if msg:  
        messages.success(request, msg)
    return render(request, 'service/home.html',)


def profile(request):
    try:
        data=user.objects.get(is_staff=True,is_superuser=False)
        
        count=Order.objects.all().count()-Order.objects.filter(status='Rejected').count()
        
        content={'data':data,       
                'count':count
        }
    except:
        data=user.objects.filter(is_staff=True,is_superuser=False).first()
        
        count=Order.objects.all().count()-Order.objects.filter(status='Rejected').count()
        
        content={'data':data,       
                'count':count
        }
     

    return render(request,'service/profile.html',content)  



@login_required
def payment(request):
    if request.user.is_authenticated and request.method=='POST':
        today=date.today()
        count=Order.objects.filter(order_date__date=today).count()        
        form =OrderCreation(request.POST)
        try:
            image=user.objects.get(is_staff=True,is_superuser=False)
            limit=image.profile.daily_limit
        except:
            image=user.objects.filter(is_staff=True,is_superuser=False).first()
            limit=image.profile.daily_limit
            
        if count >= limit:
            messages.success(request, "Daily orders limit reached. Please visit tomorrow ")
            return redirect('home')
        if form.is_valid():
            order=form.save(commit=False)
            order.customer=request.user            
            order.save()
            messages.success(request, "Your order has been placed. It takes 24 hours to process.")
            return redirect('dashboard')
        else:
            messages.warning(request, "Error has been encountered. Please contact owner.") 
            return redirect('payment')  

    else:
        today=date.today()
        count=Order.objects.filter(order_date__date=today).count()        
        form=OrderCreation()   
        try:
            image=user.objects.get(is_staff=True,is_superuser=False)
            limit=image.profile.daily_limit
            content={'image':image,
                'form':form,       
            }
        except:
            image=user.objects.filter(is_staff=True,is_superuser=False).first()
            limit=image.profile.daily_limit
            content={'image':image,
                'form':form        
            }
        if count >= limit:
            messages.success(request, "Daily orders limit reached. Please visit tomorrow ")
            return redirect('home')
        messages.warning(request, "Steps For Payment \n 1. Take ScreenShot of QR code ")    
        return render(request, 'service/order.html',content)

@login_required
def dashboard(request):
    user=request.user
    tabels=Order.objects.filter(customer=user).order_by('-order_date')
    context={'tabels':tabels}
    return render(request, 'service/dashboard.html',context)

class OrderListView(UserPassesTestMixin,ListView):    
    model = Order
    template_name = 'service/dashboard.html'         # default template format <app>/<model>_<viewtype>.html
    context_object_name='tabels'
    ordering = ['-order_date']
    def test_func(self):  
        if self.request.user.is_authenticated:
            if self.request.user.is_staff == True:
                return True
            else:
                raise Http404
        else:
            raise Http404

def OrderUpdateView(request, pk, *args, **kwargs):
    if test_func(request):
        if request.method == 'POST':
            tabels=get_object_or_404(Order, id=pk)        
            form=OrderUpdate(request.POST,instance=tabels)
            if form.is_valid():
                form.save()
                content={'tabels':tabels}
                messages.success(request, "Order Updated Successfully.")
                return render(request, 'service/order_update.html',content)   
            else:
                messages.success(request, "Caught an error. Please contact owner")
                return render(request, 'service/order_update.html',content)
        else:
            tabels=get_object_or_404(Order, id=pk)
            form=OrderUpdate()
            content={'form':form,
                'tabels':tabels
            }
            return render(request, 'service/order_update.html',content)
    else:
        raise Http404
                

           
def test_func(request):       
    if request.user.is_authenticated:
        if request.user.is_staff == True:
            return True      
        else:
            return False
    else:
        return False       

