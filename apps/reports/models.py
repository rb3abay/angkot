from django.db import models
from apps.vehicles.models import Vehicle

class DailyReport(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    report_date = models.DateField()
    total_inspections = models.IntegerField(default=0)
    passed_inspections = models.IntegerField(default=0)
    failed_inspections = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'daily_reports'
        verbose_name = 'Laporan Harian'
        verbose_name_plural = 'Laporan Harian'
        ordering = ['-report_date']
        unique_together = ['vehicle', 'report_date']
    
    def __str__(self):
        return f"Laporan Harian {self.vehicle.plate_number} - {self.report_date}"

class MonthlyReport(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_inspections = models.IntegerField(default=0)
    passed_inspections = models.IntegerField(default=0)
    failed_inspections = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    body_issues = models.IntegerField(default=0)
    windows_issues = models.IntegerField(default=0)
    tires_issues = models.IntegerField(default=0)
    interior_issues = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'monthly_reports'
        verbose_name = 'Laporan Bulanan'
        verbose_name_plural = 'Laporan Bulanan'
        ordering = ['-year', '-month']
        unique_together = ['vehicle', 'month', 'year']
    
    def __str__(self):
        month_names = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                      'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
        return f"Laporan Bulanan {self.vehicle.plate_number} - {month_names[self.month]} {self.year}"
