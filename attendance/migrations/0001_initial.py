from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True
 dependencies=[]
 operations=[
 migrations.CreateModel(name="Student",fields=[
  ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
  ("student_id",models.CharField(max_length=40,unique=True)),("name",models.CharField(max_length=120)),("email",models.EmailField(blank=True,max_length=254)),("course",models.CharField(blank=True,max_length=120)),("face_image",models.ImageField(blank=True,null=True,upload_to="faces/")),("face_encoding",models.JSONField(blank=True,null=True)),("created_at",models.DateTimeField(auto_now_add=True))]),
 migrations.CreateModel(name="AttendanceRecord",fields=[
  ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("date",models.DateField(auto_now_add=True)),("time",models.TimeField(auto_now_add=True)),("status",models.CharField(default="Present",max_length=20)),("confidence",models.FloatField(default=0)),
  ("student",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="attendance",to="attendance.student"))]),
 migrations.AddConstraint(model_name="attendancerecord",constraint=models.UniqueConstraint(fields=("student","date"),name="one_attendance_per_day"))
]