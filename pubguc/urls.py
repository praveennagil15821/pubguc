from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings                  #>for addming urlpattens of static media
from django.conf.urls.static import static        #>
from django.urls import path,include
from users import views as user_views
from service import views as service_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',user_views.signup,name='signup'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout',user_views.logout,name='logout'),
    path('profile/',user_views.profile_update,name='profile-update'),
    path('category/',user_views.CategoryListView.as_view(),name='category'),
    path('category/<int:pk>/delete',user_views.CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:pk>/update',user_views.CategoryUpdateView.as_view(), name='category-update'),
    path('category/new',user_views.CategoryCreateView.as_view(), name='category-create'),
    
#----------------------------------------------------------------------------------------------------
    path('',service_views.home,name='home'),
    path('contact/',service_views.profile,name='profile'),
    path('payment/',service_views.payment,name='payment'),
    path('dashboard/',service_views.dashboard,name='dashboard'),
    path('is?root?ki?4sabhi?6line?m?ghusne?wale?savdhan?/',service_views.OrderListView.as_view(),name='dash'),
    path('is?root?ki?4sabhi?6line?m?ghusne?wale?savdhan?/<int:pk>/update',service_views.OrderUpdateView, name='order-update'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
