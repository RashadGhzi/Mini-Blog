from core import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('blogupdate/<int:id>/', views.blog_update, name='blogUpdate'),
    path('blogdelete/<int:id>/', views.blog_delete, name="blogDelete")
]
