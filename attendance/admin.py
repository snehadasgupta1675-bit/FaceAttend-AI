from django.contrib import admin
from .models import Student,AttendanceRecord
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
 list_display=("student_id","name","course","created_at")
 search_fields=("student_id","name","email")
@admin.register(AttendanceRecord)
class AttendanceAdmin(admin.ModelAdmin):
 list_display=("student","date","time","status","confidence")
 list_filter=("date","status")
