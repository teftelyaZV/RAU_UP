from django.urls import path
from system_app import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('tech/', views.tech_dashboard, name='tech_dashboard'),
    path('logout/', views.logout, name='logout'),
]