# FaceAttend-AI

## AI-Based Face Recognition Attendance Management System

FaceAttend-AI is a web-based attendance management system developed using **Django, Python, OpenCV, HTML, CSS, and JavaScript**.

The system allows users to register students, create live face profiles using the device camera, and mark daily attendance through face recognition.

The project is designed to make attendance management simple, fast, and organized without requiring manual attendance entry.

---

## 🌐 Live Demo

**Live Website:**  
https://faceattend-ai-b9ke.onrender.com

---

## 📌 Project Overview

FaceAttend-AI provides a simple web interface for managing student attendance using facial recognition technology.

The system has two main processes:

1. **Student Registration**
2. **Face Profile Creation and Attendance Recognition**

A student is first registered with their basic details. A live camera frame is then captured to create the student's face profile. During attendance, another live camera frame is captured and compared with the saved face profiles.

If a matching face is found with sufficient confidence, the student's attendance is recorded for the current date.

---

## ✨ Features

- Student registration
- Student ID management
- Student name and email details
- Live camera face capture
- Face profile creation
- Face detection using OpenCV
- Face recognition and matching
- Daily attendance marking
- Attendance date and time recording
- Recognition confidence percentage
- Prevention of duplicate attendance on the same day
- Student deletion
- Attendance records table
- Login and registration system
- Responsive web interface
- Django-based backend
- Deployable on Render

---

## 🖥️ Main Pages

### Home

Provides an introduction to FaceAttend-AI and explains the purpose of the system.

### About

Provides information about the project and its purpose.

### Features

Displays the major features available in the system.

### Students

Allows the user to:

- View registered students
- Add new students
- View student information
- Delete students

### Attendance

The Attendance page is the main camera-based section.

It allows the user to:

- Start the live camera
- Select a registered student
- Create a face profile
- Capture a fresh face frame
- Recognize a registered student
- Mark attendance
- View today's attendance records

### Login / Register

Provides user authentication for accessing the attendance management system.

---

## 🔄 System Workflow

```text
User Login
     ↓
Student Registration
     ↓
Open Attendance Page
     ↓
Start Live Camera
     ↓
Select Student
     ↓
Capture Face Profile
     ↓
Face Detection
     ↓
Save Face Profile
     ↓
Take Fresh Live Face
     ↓
Face Recognition
     ↓
Compare With Registered Profiles
     ↓
Matching Student Found
     ↓
Attendance Marked
     ↓
Attendance Record Displayed
