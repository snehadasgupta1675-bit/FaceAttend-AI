from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone
from django.core.files.base import ContentFile
import base64
import uuid

from .forms import RegisterForm, StudentForm
from .models import Student, AttendanceRecord
from .face_utils import extract_face_signature, compare_signatures


def camera_image(data_url):
    if not data_url or not data_url.startswith("data:image/"):
        raise ValueError("Please capture a face using the live camera.")
    try:
        _, encoded = data_url.split(",", 1)
        raw = base64.b64decode(encoded)
    except Exception as exc:
        raise ValueError("The camera image could not be read. Please capture it again.") from exc
    return ContentFile(raw, name=f"camera_{uuid.uuid4().hex}.jpg")


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def features(request):
    return render(request, "features.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("attendance")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please sign in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "auth.html", {"form": form, "mode": "register"})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("attendance")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect("attendance")
        messages.error(request, "Invalid username or password.")
    return render(request, "auth.html", {"mode": "login"})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def students(request):
    return render(request, "students.html", {"students": Student.objects.order_by("name")})


@login_required
def add_student(request):
    """Create only the student record. Face capture happens exclusively on Attendance."""
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                messages.success(request, f"{student.name} was registered. Now open Attendance to create the live face profile.")
                return redirect("students")
            except IntegrityError:
                form.add_error("student_id", "This Student ID is already registered.")
    else:
        form = StudentForm()
    return render(request, "add_student.html", {"form": form})


@login_required
def delete_student(request, student_id):
    if request.method == "POST":
        student = get_object_or_404(Student, id=student_id)
        name = student.name
        student.delete()
        messages.success(request, f"{name} and their attendance history were deleted.")
    return redirect("students")


@login_required
def attendance(request):
    result = None
    profile_result = None

    if request.method == "POST":
        action = request.POST.get("action", "mark")
        try:
            signature = extract_face_signature(camera_image(request.POST.get("face_image_data")))

            if action == "enroll":
                student_id = request.POST.get("student_id")
                student = get_object_or_404(Student, id=student_id)
                student.face_encoding = signature
                student.save(update_fields=["face_encoding"])
                profile_result = {"student": student}
                messages.success(request, f"Live face profile saved for {student.name}. You can now mark attendance.")
            else:
                known_students = list(Student.objects.exclude(face_encoding=None))
                if not known_students:
                    messages.warning(request, "No face profiles are ready. Select a registered student and save their live face profile first.")
                else:
                    best, confidence = max(
                        ((s, compare_signatures(s.face_encoding, signature)) for s in known_students),
                        key=lambda item: item[1],
                    )
                    if confidence >= 82:
                        try:
                            record, created = AttendanceRecord.objects.get_or_create(
                                student=best,
                                date=timezone.localdate(),
                                defaults={"status": "Present", "confidence": confidence},
                            )
                        except IntegrityError:
                            record = AttendanceRecord.objects.get(student=best, date=timezone.localdate())
                            created = False
                        result = {"student": best, "confidence": confidence, "already": not created}
                    else:
                        messages.warning(request, "Face not recognized with enough confidence. Please look at the camera and try again.")
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception:
            messages.error(request, "Face processing failed. Please allow camera access and try again.")

    students_list = list(Student.objects.order_by("name"))
    records = AttendanceRecord.objects.filter(date=timezone.localdate()).select_related("student").order_by("-time")
    return render(request, "attendance.html", {
        "records": records,
        "result": result,
        "profile_result": profile_result,
        "students": students_list,
        "today": timezone.localdate(),
    })
