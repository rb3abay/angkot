from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DailyReport, MonthlyReport
from apps.inspections.models import Inspection
from apps.vehicles.models import Vehicle
import os
import tempfile

@login_required(login_url='users:login')
def report_dashboard_view(request):
    """Dashboard laporan dengan statistik"""
    today = timezone.now().date()
    
    # Statistik hari ini
    today_inspections = Inspection.objects.filter(inspection_date__date=today)
    total_today = today_inspections.count()
    
    passed_today = sum(1 for i in today_inspections if i.calculate_score() >= 70)
    failed_today = total_today - passed_today
    avg_today = sum(i.calculate_score() for i in today_inspections) / total_today if total_today > 0 else 0
    
    # Statistik minggu ini
    week_start = today - timedelta(days=today.weekday())
    week_inspections = Inspection.objects.filter(inspection_date__date__gte=week_start)
    total_week = week_inspections.count()
    
    # Statistik bulan ini
    month_start = today.replace(day=1)
    month_inspections = Inspection.objects.filter(inspection_date__date__gte=month_start)
    total_month = month_inspections.count()
    
    # Top vehicles
    top_vehicles = Vehicle.objects.annotate(
        inspection_count=Count('inspection')
    ).order_by('-inspection_count')[:5]
    
    context = {
        'total_today': total_today,
        'passed_today': passed_today,
        'failed_today': failed_today,
        'avg_today': round(avg_today, 1),
        'total_week': total_week,
        'total_month': total_month,
        'top_vehicles': top_vehicles,
        'recent_inspections': Inspection.objects.all()[:10],
    }
    return render(request, 'reports/report_dashboard.html', context)

@login_required(login_url='users:login')
def daily_report_list_view(request):
    """Daftar laporan harian"""
    reports = DailyReport.objects.all()
    
    # Filter berdasarkan tanggal
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if date_from:
        reports = reports.filter(report_date__gte=date_from)
    if date_to:
        reports = reports.filter(report_date__lte=date_to)
    
    context = {
        'reports': reports,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'reports/daily_report_list.html', context)

@login_required(login_url='users:login')
def daily_report_detail_view(request, report_id):
    """Detail laporan harian"""
    report = get_object_or_404(DailyReport, pk=report_id)
    inspections = Inspection.objects.filter(
        vehicle=report.vehicle,
        inspection_date__date=report.report_date
    )
    
    context = {
        'report': report,
        'inspections': inspections,
    }
    return render(request, 'reports/daily_report_detail.html', context)

@login_required(login_url='users:login')
def monthly_report_list_view(request):
    """Daftar laporan bulanan"""
    reports = MonthlyReport.objects.all()
    
    # Filter berdasarkan bulan dan tahun
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if month:
        reports = reports.filter(month=month)
    if year:
        reports = reports.filter(year=year)
    
    context = {
        'reports': reports,
        'month': month,
        'year': year,
        'months': range(1, 13),
        'years': range(datetime.now().year - 5, datetime.now().year + 1),
    }
    return render(request, 'reports/monthly_report_list.html', context)

@login_required(login_url='users:login')
def monthly_report_detail_view(request, report_id):
    """Detail laporan bulanan"""
    report = get_object_or_404(MonthlyReport, pk=report_id)
    
    context = {
        'report': report,
    }
    return render(request, 'reports/monthly_report_detail.html', context)
