from django.db import models
class Student(models.Model):
    student_id=models.CharField(max_length=40,unique=True)
    name=models.CharField(max_length=120)
    email=models.EmailField(blank=True)
    course=models.CharField(max_length=120,blank=True)
    face_encoding=models.JSONField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.student_id} - {self.name}"
class AttendanceRecord(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="attendance")
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    status=models.CharField(max_length=20,default="Present")
    confidence=models.FloatField(default=0)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["student","date"],name="one_attendance_per_day")]
    def __str__(self): return f"{self.student.name} - {self.date}"
