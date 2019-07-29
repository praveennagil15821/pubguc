from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout as log
from django.contrib.auth.mixins import UserPassesTestMixin
from . forms import CustomUserCreationForm,ProfileUpdateForm,CategoryUpdateForm
from django.shortcuts import render, redirect
from django.contrib import messages
from service.models import *
from users.models import CustomUser as user 
from datetime import date
from django.views.generic import (
        ListView,        
        CreateView,
        UpdateView,
        DeleteView,
        )

#---------------------------------------------------------------------------------------
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            messages.success(request, "Registered successfully. You can now login")
            return redirect('login')

    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        log(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('home')      
    else:
        raise Http404

def profile_update(request):
    if request.user.is_staff == True:
        if request.method == 'POST':        
            
            try:
                p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)   #want current pic detail instance=request.user.profile
            except:
                messages.error(request, "Please create your profile first. Contact owner.")
                return redirect('home')

            if p_form.is_valid():                
                p_form.save()
                messages.success(request,f'Your Profile has been Updated!')
                return redirect('profile-update')

        else:
            p_form = ProfileUpdateForm()   #want current pic detail instance=request.user.profile           
            try:
                data=user.objects.filter(is_staff=True,is_superuser=False).first()              
                count=Order.objects.all().count()-Order.objects.filter(status='Rejected').count()   
                today=date.today()
                today_count=Order.objects.filter(order_date__date=today).count() 
                content={'data':data,       
                        'count':count,
                        'p_form':p_form,
                        'today_count':today_count,
                }
            except:
                messages.error(request, "Staff user not found. Make shure only one staff user is created except admin.")
                return redirect('home')  

            return render(request,'service/profile.html',content)
    else:        
        raise Http404

class CategoryListView(UserPassesTestMixin,ListView):
    model = Category
    template_name = 'service/profile_category.html'         # default template format <app>/<model>_<viewtype>.html
    context_object_name='datas'
    ordering = ['price']

    def test_func(self):  
        if self.request.user.is_authenticated:
            if self.request.user.is_staff == True:
                return True
            else:
                raise Http404
        else:
            raise Http404


class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['title','price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  
        if self.request.user.is_authenticated:
            if self.request.user.is_staff == True:
                return True
            else:
                raise Http404
        else:
            raise Http404
class CategoryCreateView(UserPassesTestMixin, CreateView):
    model = Category
    fields = ['title','price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  
        if self.request.user.is_authenticated:
            if self.request.user.is_staff == True:
                return True
            else:
                raise Http404
        else:
            raise Http404

class CategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = Category
    success_url = '/category'
    def test_func(self):  
        if self.request.user.is_authenticated:
            if self.request.user.is_staff == True:
                return True
            else:
                raise Http404
        else:
            raise Http404
          