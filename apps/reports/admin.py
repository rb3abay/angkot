from django.contrib import admin
from .models import DailyReport, MonthlyReport

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('get_plate_number', 'report_date', 'total_inspections', 'passed_inspections', 'average_score')
    list_filter = ('report_date', 'vehicle__plate_number')
    search_fields = ('vehicle__plate_number',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_plate_number(self, obj):
        return obj.vehicle.plate_number
    get_plate_number.short_description = 'Plat Nomor'

@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('get_plate_number', 'month', 'year', 'total_inspections', 'passed_inspections', 'average_score')
    list_filter = ('year', 'month', 'vehicle__plate_number')
    search_fields = ('vehicle__plate_number',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_plate_number(self, obj):
        return obj.vehicle.plate_number
    get_plate_number.short_description = 'Plat Nomor'
