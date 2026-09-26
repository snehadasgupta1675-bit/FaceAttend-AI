# FaceAttend AI

Camera-based facial recognition attendance system built with Django.

## Main navigation
Home | About | Features | Attendance | Students | Sign out

For signed-out users: Home | About | Features | Sign in

## Camera workflow
1. Create an account and sign in.
2. Open Students → Register a student.
3. Enter student details and capture one face from the live camera. No image upload is used.
4. Open Attendance → Start camera → Take face & mark attendance.
5. A recognized student is recorded once per day.
6. Students can be deleted from the Students page; their attendance history is deleted with them.

## Windows local setup
Open Command Prompt/VS Code terminal in the folder containing `manage.py`:

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Camera note
The browser must be allowed to use the camera. Localhost works for browser camera access. On a deployed site, use HTTPS.

## Deployment
The included `render.yaml` provides a basic Render web service configuration.
