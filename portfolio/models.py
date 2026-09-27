from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    name = models.CharField(max_length=100, default="ISREL")
    title = models.CharField(max_length=200, default="Aspiring Web Developer & Data Science Enthusiast")
    summary = models.TextField(
        default="Passionate Web Developer and Data Science Enthusiast currently pursuing a B.Tech in Computer Science "
                "(Data Science specialization) at SRM University. Skilled in Python, Front-End Development, and Data Analysis. "
                "Dedicated to building user-friendly, data-driven solutions."
    )
    career_objective = models.TextField(
        default="To grow as a Web Developer & Data Scientist, contributing to innovative projects that combine "
                "creativity, data, and technology while continuously learning in a dynamic environment."
    )
    location = models.CharField(max_length=150, default="Chennai, Tamil Nadu, India")
    email = models.EmailField(default="makportx@gmail.com")
    linkedin = models.URLField(default="https://linkedin.com/in/isrel")
    github = models.URLField(default="https://github.com/makportx")
    available_for_opportunities = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Personal Profile"
        verbose_name_plural = "Personal Profile"

    def __str__(self):
        return f"{self.name} - {self.title}"


class Education(models.Model):
    institution = models.CharField(max_length=200, default="SRM Institute of Science and Technology (SRMIST)")
    degree = models.CharField(max_length=150, default="B.Tech in Computer Science")
    specialization = models.CharField(max_length=150, default="Data Science specialization")
    graduation_date = models.CharField(max_length=100, default="Expected Graduation: May 2029")
    description = models.TextField(
        blank=True,
        default="Focusing on core computer science foundations, algorithms, machine learning, data engineering, and modern web architectures."
    )
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('programming', 'Programming'),
        ('data_science', 'Data Science & AI'),
        ('tools', 'Tools & Workflow'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='web')
    name = models.CharField(max_length=100)
    level_note = models.CharField(max_length=50, blank=True, help_text="e.g., 'Proficient', 'Intermediate', 'basics'")
    proficiency = models.PositiveIntegerField(default=85, help_text="Percentage 0-100 for visual bar")
    icon_name = models.CharField(max_length=50, default="code", help_text="Lucide icon name")
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('ai_ml', 'AI & Machine Learning'),
        ('fullstack', 'Web Development & Full Stack'),
        ('data_science', 'Data Science & Dashboards'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='fullstack')
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    extended_details = models.TextField(
        blank=True,
        help_text="Detailed project breakdown, challenges, solutions, and impact."
    )
    tech_stack = models.CharField(max_length=255, help_text="Comma-separated technologies, e.g. Python, OpenCV, Tkinter")
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=True)
    icon_name = models.CharField(max_length=50, default="folder", help_text="Lucide icon name")
    created_at = models.DateField(auto_now_add=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tech_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]

    def __str__(self):
        return self.title


class Strength(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default="check-circle-2")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - {self.created_at.strftime('%b %d, %Y')}"
