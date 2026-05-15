from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from apps.vehicles.models import Vehicle
from apps.inspections.models import Inspection
from apps.users.models import CustomUser
from datetime import datetime, timedelta
from django.utils import timezone

@login_required(login_url='users:login')
def dashboard_view(request):
    """Dashboard utama aplikasi"""
    today = timezone.now().date()
    
    # Statistik Kendaraan
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(status='active').count()
    maintenance_vehicles = Vehicle.objects.filter(status='maintenance').count()
    inactive_vehicles = Vehicle.objects.filter(status='inactive').count()
    
    # Statistik Petugas
    total_officers = CustomUser.objects.filter(role='officer').count()
    active_officers = CustomUser.objects.filter(role='officer', is_active=True).count()
    
    # Statistik Inspeksi Hari Ini
    today_inspections = Inspection.objects.filter(inspection_date__date=today)
    total_today = today_inspections.count()
    
    passed_today = sum(1 for i in today_inspections if i.calculate_score() >= 70)
    failed_today = total_today - passed_today
    avg_today = sum(i.calculate_score() for i in today_inspections) / total_today if total_today > 0 else 0
    
    # Statistik Minggu Ini
    week_start = today - timedelta(days=today.weekday())
    week_inspections = Inspection.objects.filter(inspection_date__date__gte=week_start)
    total_week = week_inspections.count()
    
    # Statistik Bulan Ini
    month_start = today.replace(day=1)
    month_inspections = Inspection.objects.filter(inspection_date__date__gte=month_start)
    total_month = month_inspections.count()
    
    # 10 Inspeksi Terakhir
    recent_inspections = Inspection.objects.all()[:10]
    
    # Top Vehicles (paling sering diinspeksi)
    top_vehicles = Vehicle.objects.annotate(
        inspection_count=Count('inspection')
    ).order_by('-inspection_count')[:5]
    
    # Top Officers (paling banyak inspeksi)
    top_officers = CustomUser.objects.annotate(
        inspection_count=Count('inspection')
    ).order_by('-inspection_count')[:5]
    
    # Vehicle Status Pie Chart Data
    vehicle_status_data = {
        'active': active_vehicles,
        'maintenance': maintenance_vehicles,
        'inactive': inactive_vehicles,
    }
    
    # Inspection Score Distribution
    passed_inspections = sum(1 for i in month_inspections if i.calculate_score() >= 70)
    failed_inspections = total_month - passed_inspections
    
    context = {
        # Kendaraan
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'maintenance_vehicles': maintenance_vehicles,
        'inactive_vehicles': inactive_vehicles,
        'vehicle_status_data': vehicle_status_data,
        
        # Petugas
        'total_officers': total_officers,
        'active_officers': active_officers,
        
        # Inspeksi Hari Ini
        'total_today': total_today,
        'passed_today': passed_today,
        'failed_today': failed_today,
        'avg_today': round(avg_today, 1),
        
        # Inspeksi Minggu/Bulan
        'total_week': total_week,
        'total_month': total_month,
        'passed_month': passed_inspections,
        'failed_month': failed_inspections,
        
        # Top Data
        'recent_inspections': recent_inspections,
        'top_vehicles': top_vehicles,
        'top_officers': top_officers,
    }
    
    return render(request, 'dashboard/index.html', context)
