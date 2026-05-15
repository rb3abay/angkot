from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_dashboard_view, name='dashboard'),
    path('daily/', views.daily_report_list_view, name='daily-list'),
    path('daily/<int:report_id>/', views.daily_report_detail_view, name='daily-detail'),
    path('monthly/', views.monthly_report_list_view, name='monthly-list'),
    path('monthly/<int:report_id>/', views.monthly_report_detail_view, name='monthly-detail'),
]
