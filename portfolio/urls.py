from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('resume/', views.resume_view, name='resume'),
    path('project/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('contact/submit/', views.contact_submit_view, name='contact_submit'),
    path('api/ai-assistant/', views.ai_assistant_api, name='ai_assistant_api'),
    path('favicon.ico', views.favicon_view, name='favicon'),
]
