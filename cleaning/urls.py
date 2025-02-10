from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_request/', views.create_request, name='create_request'),
    path('request_list/', views.request_list, name='request_list'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('change_status/<int:request_id>/', views.change_status, name='change_status'),
]
