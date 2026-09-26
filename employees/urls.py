from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('employees/', views.emp_list, name='emp_list'),
    path('employees/add/', views.emp_create, name='emp_create'),
    path('employees/<int:pk>/', views.emp_detail, name='emp_detail'),
    path('employees/<int:pk>/edit/', views.emp_update, name='emp_update'),
    path('employees/<int:pk>/delete/', views.emp_delete, name='emp_delete'),

    path('payslip/generate/', views.generate_payslip, name='generate_payslip'),
    path('payslip/<int:pk>/', views.payslip_detail, name='payslip_detail'),
    path('payslips/', views.payslip_history, name='payslip_history'),
]