from django import forms
from django.contrib.auth.models import User
from .models import Student
class RegisterForm(forms.ModelForm):
 password=forms.CharField(widget=forms.PasswordInput)
 confirm_password=forms.CharField(widget=forms.PasswordInput)
 class Meta:
  model=User; fields=["username","email","password"]
 def clean(self):
  d=super().clean()
  if d.get("password")!=d.get("confirm_password"): raise forms.ValidationError("Passwords do not match.")
  return d
 def save(self,commit=True):
  u=super().save(commit=False); u.set_password(self.cleaned_data["password"])
  if commit:u.save()
  return u
class StudentForm(forms.ModelForm):
 class Meta:
  model=Student; fields=["student_id","name","email","course"]
