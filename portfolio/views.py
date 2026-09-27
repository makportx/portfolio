import json
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

def favicon_view(request):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#06b6d4"/><text x="50%" y="55%" font-family="system-ui, sans-serif" font-weight="900" font-size="38" fill="#020617" text-anchor="middle" dominant-baseline="middle">I</text></svg>'
    return HttpResponse(svg, content_type="image/svg+xml")


from .models import Profile, Education, Skill, Project, Strength, ContactMessage
from .forms import ContactForm


def get_or_create_default_profile():
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(
            name="ISREL",
            title="Aspiring Web Developer & Data Science Enthusiast",
            location="Chennai, Tamil Nadu, India",
            email="makportx@gmail.com",
            linkedin="https://linkedin.com/in/isrel",
            github="https://github.com/makportx"
        )
    return profile


def home_view(request):
    profile = get_or_create_default_profile()
    education_list = Education.objects.all()
    skills_qs = Skill.objects.all()
    projects = Project.objects.all()
    strengths = Strength.objects.all()

    # Group skills by category for display
    skills_by_category = {
        'web': skills_qs.filter(category='web'),
        'programming': skills_qs.filter(category='programming'),
        'data_science': skills_qs.filter(category='data_science'),
        'tools': skills_qs.filter(category='tools'),
    }

    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent to Isrel. I'll get back to you shortly.")
            return redirect('home')
        else:
            messages.error(request, "Please check the form for errors.")

    context = {
        'profile': profile,
        'education_list': education_list,
        'skills_by_category': skills_by_category,
        'all_skills': skills_qs,
        'projects': projects,
        'strengths': strengths,
        'form': form,
    }
    return render(request, 'portfolio/index.html', context)


def project_detail_view(request, slug):
    profile = get_or_create_default_profile()
    project = get_object_or_404(Project, slug=slug)
    other_projects = Project.objects.exclude(id=project.id)[:3]
    return render(request, 'portfolio/project_detail.html', {
        'profile': profile,
        'project': project,
        'other_projects': other_projects,
    })


def resume_view(request):
    profile = get_or_create_default_profile()
    education_list = Education.objects.all()
    skills_qs = Skill.objects.all()
    projects = Project.objects.all()
    strengths = Strength.objects.all()

    skills_by_category = {
        'Web Development': skills_qs.filter(category='web'),
        'Programming': skills_qs.filter(category='programming'),
        'Data Science': skills_qs.filter(category='data_science'),
        'Tools': skills_qs.filter(category='tools'),
    }

    return render(request, 'portfolio/resume.html', {
        'profile': profile,
        'education_list': education_list,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'strengths': strengths,
    })


@require_POST
def contact_submit_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
                form = ContactForm(data)
            else:
                form = ContactForm(request.POST)

            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'ok', 'message': "Thank you! Your message has been received."})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Thank you! Your message has been sent.")
    else:
        messages.error(request, "Failed to send message. Please review the form.")
    return redirect('home')


@csrf_protect
def ai_assistant_api(request):
    """
    Interactive AI resume assistant widget endpoint.
    Answers inquiries regarding Isrel's background, education, projects, skills, and goals.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_query = data.get('query', '').strip().lower()
    except Exception:
        user_query = request.POST.get('query', '').strip().lower()

    if not user_query:
        return JsonResponse({'response': "Hello! I'm Isrel's AI Portfolio Assistant. Ask me anything about Isrel's education, skills, projects, or how to get in touch!"})

    # Knowledge base queries
    if any(k in user_query for k in ['education', 'college', 'university', 'srm', 'degree', 'study', 'graduat']):
        reply = (
            "🎓 **Education Background**:\n"
            "Isrel is currently pursuing a **B.Tech in Computer Science (Data Science specialization)** "
            "at **SRM Institute of Science and Technology (SRMIST)**, Chennai.\n"
            "Expected graduation is **May 2029**."
        )
    elif any(k in user_query for k in ['skill', 'stack', 'tech', 'language', 'python', 'django', 'react', 'tools']):
        reply = (
            "💻 **Technical Skills**:\n"
            "• **Web Development**: Django, HTML5, CSS3, JavaScript, React\n"
            "• **Programming**: Python, C/C++ (basics)\n"
            "• **Data Science**: Data Analysis, Data Visualization (pandas, matplotlib), Computer Vision (OpenCV)\n"
            "• **Tools**: Git, GitHub, VS Code, Django Admin & ORM"
        )
    elif any(k in user_query for k in ['project', 'face recognition', 'attendance', 'dashboard', 'assistant', 'work']):
        reply = (
            "🚀 **Key Projects**:\n\n"
            "1. **Face Recognition Attendance System**: AI-powered biometric attendance tracker using OpenCV (cv2) with a Tkinter desktop GUI for real-time recognition.\n"
            "2. **Portfolio Website with AI Assistant**: Multi-page portfolio built with React, Node.js, MongoDB, and an intelligent assistant.\n"
            "3. **Data Dashboards (Practice Projects)**: Interactive data dashboards built using Python (pandas, matplotlib) for exploratory data visualization.\n"
            "4. **Django Portfolio Application**: This dynamic web app featuring Django ORM models, an administration dashboard, and resume integration."
        )
    elif any(k in user_query for k in ['contact', 'email', 'hire', 'reach', 'message', 'phone', 'linkedin', 'location', 'github']):
        reply = (
            "📫 **Get in Touch with Isrel**:\n"
            "• **Email**: [makportx@gmail.com](mailto:makportx@gmail.com)\n"
            "• **LinkedIn**: [linkedin.com/in/isrel](https://linkedin.com/in/isrel)\n"
            "• **GitHub**: [github.com/makportx](https://github.com/makportx)\n"
            "• **Location**: Chennai, Tamil Nadu, India\n"
            "You can also use the contact form at the bottom of this page to send a direct message!"
        )
    elif any(k in user_query for k in ['strength', 'advantage', 'mindset', 'soft skill']):
        reply = (
            "⭐ **Core Strengths**:\n"
            "✔ Strong problem-solving mindset\n"
            "✔ Quick adaptability to new technologies\n"
            "✔ Passion for merging design aesthetics with solid engineering\n"
            "✔ Interest in both software development and data-driven insights"
        )
    elif any(k in user_query for k in ['goal', 'career', 'objective', 'future']):
        reply = (
            "🎯 **Career Objective**:\n"
            "To grow as a Web Developer & Data Scientist, contributing to innovative projects that combine "
            "creativity, data, and technology while continuously learning in a dynamic environment."
        )
    elif any(k in user_query for k in ['hi', 'hello', 'hey', 'who are you']):
        reply = (
            "👋 Hi there! I'm Isrel's AI Portfolio Assistant.\n"
            "You can ask me about:\n"
            "• Isrel's projects (Face Recognition, Dashboards, Web apps)\n"
            "• Education at SRMIST\n"
            "• Technical skills in Python, Django, React, and Data Science\n"
            "• How to contact Isrel"
        )
    else:
        reply = (
            f"Thanks for asking! Isrel is an aspiring Web Developer & Data Science enthusiast studying at SRMIST "
            f"with strong experience in Python, Django, React, and Data Science.\n\n"
            f"Feel free to ask about his projects, education, technical skills, or send him a message through the contact form!"
        )

    return JsonResponse({'response': reply})
