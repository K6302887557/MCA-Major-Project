from django.urls import path
from .import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('home_page/', views.home_page, name='home_page'),
    path('manage_details/', views.manage_details, name='manage_details'),
    path('delete_file/<int:file_id>', views.delete_file, name='delete_file'),
    path('logout/', views.logout, name='logout'),
]