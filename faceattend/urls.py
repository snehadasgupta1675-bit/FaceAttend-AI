from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from attendance import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("features/", views.features, name="features"),
    path("attendance/", views.attendance, name="attendance"),
    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/delete/<int:student_id>/", views.delete_student, name="delete_student"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
