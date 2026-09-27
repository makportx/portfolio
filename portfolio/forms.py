from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-700/80 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition duration-200',
                'placeholder': 'Your full name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-700/80 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition duration-200',
                'placeholder': 'your.email@example.com',
                'required': True,
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-700/80 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition duration-200',
                'placeholder': 'Project inquiry / Opportunity / Collaboration',
                'required': False,
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-700/80 text-slate-100 placeholder-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition duration-200 resize-none',
                'rows': 5,
                'placeholder': 'Hi Isrel, I would love to connect with you regarding...',
                'required': True,
            }),
        }
