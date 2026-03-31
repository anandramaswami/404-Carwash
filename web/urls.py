from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('services/', views.services, name='services'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('payment/', views.process_payment, name='process_payment'),
    
    # Admin routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/customers/', views.dashboard_customers, name='dashboard_customers'),
    path('admin-dashboard/bookings/', views.dashboard_bookings, name='dashboard_bookings'),
    path('admin-dashboard/services/', views.dashboard_services, name='dashboard_services'),
    path('admin-dashboard/parkings/', views.dashboard_parkings, name='dashboard_parkings'),
]
