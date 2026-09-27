from django.contrib import admin
from .models import Profile, Education, Skill, Project, Strength, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'location', 'available_for_opportunities')
    fieldsets = (
        ("Personal Information", {
            'fields': ('name', 'title', 'location', 'available_for_opportunities')
        }),
        ("Summary & Objective", {
            'fields': ('summary', 'career_objective')
        }),
        ("Contact & Socials", {
            'fields': ('email', 'linkedin', 'github')
        }),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'specialization', 'graduation_date', 'order')
    list_editable = ('order',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level_note', 'proficiency', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'level_note')
    list_editable = ('proficiency', 'is_featured', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'tech_stack', 'order', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'order')


@admin.register(Strength)
class StrengthAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
