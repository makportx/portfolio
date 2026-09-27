# ISREL — Modern Django Portfolio & Resume Engine

[![Live Portfolio](https://img.shields.io/badge/Live_Portfolio-GitHub_Pages-cyan?style=for-the-badge&logo=github)](https://makportx.github.io/portfolio/)
[![Django](https://img.shields.io/badge/Django-6.1-emerald?style=for-the-badge&logo=django)](https://djangoproject.com)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-blue?style=for-the-badge&logo=githubactions)](https://github.com/makportx/portfolio/actions)

🌐 **Live Demo URL**: [https://makportx.github.io/portfolio/](https://makportx.github.io/portfolio/)

A dynamic, production-ready personal portfolio web application built with **Django 6**, **Tailwind CSS**, and **SQLite**. Fully customized and populated with **Isrel's** resume (B.Tech in Computer Science with Data Science specialization at SRMIST).

---


## 🌟 Key Features

1. **Resume-Driven Dynamic Content**:
   - Built on Django ORM models: `Profile`, `Education`, `Skill`, `Project`, `Strength`, and `ContactMessage`.
   - Pre-populated with Isrel's background:
     - **Education**: SRM Institute of Science and Technology (SRMIST) &bull; B.Tech CSE (Data Science) &bull; Graduation May 2029.
     - **Projects**:
       - *Face Recognition Attendance System* (AI / OpenCV / Tkinter)
       - *Portfolio Website with AI Assistant* (React / Node.js / MongoDB)
       - *Data Dashboards* (Python / Pandas / Matplotlib)
       - *Django Portfolio & CMS Engine* (Django 6 / SQLite / Tailwind)
     - **Skills**: Web Development (Django, React, HTML, CSS, JS), Programming (Python, C/C++), Data Science (Pandas, Matplotlib, OpenCV), Tools (Git/GitHub, VS Code).
     - **Strengths**: Problem solving, quick adaptability, merging design with functionality, development & data insights.

2. **Interactive AI Resume Assistant**:
   - Floating AI assistant widget that answers visitor queries about Isrel's background, technical skills, projects, and contact info.

3. **Printable Resume View (`/resume/`)**:
   - Pixel-perfect, printer-friendly clean resume page replicating the provided resume format with a 1-click **"Print / Save as PDF"** button.

4. **Working Contact Form**:
   - Validated Django `ModelForm` that saves incoming inquiries to the database for easy retrieval.

5. **Full Django Admin Suite (`/admin/`)**:
   - Customized admin dashboard to manage projects, update skills, change career objectives, and review received contact messages.

---

## 🚀 Quick Start Guide

### 1. Navigate to the project directory:
```bash
cd django_portfolio
```

### 2. Run Database Migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 3. Seed Isrel's Resume Data:
Populate the database with all the resume information instantly:
```bash
python3 manage.py seed_portfolio
```

### 4. Create an Admin Account (Optional):
```bash
python3 manage.py createsuperuser
```

### 5. Start the Development Server:
```bash
python3 manage.py runserver
```
Visit **http://127.0.0.1:8000/** in your browser!

---

## 🧭 Application Routes

- **`/`**: Main Portfolio landing page (Hero, Education, Skills, Featured Projects, Strengths, Contact Form, AI Assistant).
- **`/resume/`**: Clean printable resume view with PDF export.
- **`/project/<slug>/`**: Deep-dive case study page for individual projects.
- **`/admin/`**: Django Administration Dashboard.
- **`/api/ai-assistant/`**: Interactive assistant API endpoint.

---

## 🧪 Running Automated Tests

Run the test suite covering models, views, forms, and the AI assistant:
```bash
python3 manage.py test
```
