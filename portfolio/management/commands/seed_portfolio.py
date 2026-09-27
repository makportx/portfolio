from django.core.management.base import BaseCommand
from django.utils.text import slugify
from portfolio.models import Profile, Education, Skill, Project, Strength


class Command(BaseCommand):
    help = "Seeds the database with Isrel's resume profile, skills, projects, and education"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding portfolio data from Isrel's resume..."))

        # 1. Profile
        Profile.objects.all().delete()
        profile = Profile.objects.create(
            name="ISREL",
            title="Aspiring Web Developer & Data Science Enthusiast",
            summary=(
                "Passionate Web Developer and Data Science Enthusiast currently pursuing a B.Tech in Computer Science "
                "(Data Science specialization) at SRM University. Skilled in Python, Front-End Development, and Data Analysis. "
                "Dedicated to building user-friendly, data-driven solutions."
            ),
            career_objective=(
                "To grow as a Web Developer & Data Scientist, contributing to innovative projects that combine "
                "creativity, data, and technology while continuously learning in a dynamic environment."
            ),
            location="Chennai, Tamil Nadu, India",
            email="makportx@gmail.com",
            linkedin="https://linkedin.com/in/isrel",
            github="https://github.com/makportx",
            available_for_opportunities=True,
        )
        self.stdout.write(self.style.SUCCESS("✓ Profile created"))

        # 2. Education
        Education.objects.all().delete()
        Education.objects.create(
            institution="SRM Institute of Science and Technology (SRMIST)",
            degree="B.Tech in Computer Science",
            specialization="Data Science specialization",
            graduation_date="Expected Graduation: May 2029",
            description=(
                "Undergraduate program focusing on core computer science foundations, algorithms, object-oriented programming, "
                "machine learning fundamentals, database management systems, and specialized data science topics."
            ),
            order=1
        )
        self.stdout.write(self.style.SUCCESS("✓ Education records created"))

        # 3. Technical Skills
        Skill.objects.all().delete()
        skills_data = [
            # Web Development
            ('web', 'HTML5', 'Semantic & accessible web markup', 95, 'code-2', 1),
            ('web', 'CSS3 / Tailwind', 'Responsive design & modern styling', 90, 'palette', 2),
            ('web', 'JavaScript', 'Modern ES6+, DOM manipulation & async logic', 88, 'file-code-2', 3),
            ('web', 'React', 'Component-based UI development & state management', 82, 'atom', 4),
            ('web', 'Django', 'Full-stack MVC/MVT web apps, ORM & REST APIs', 86, 'server', 5),

            # Programming
            ('programming', 'Python', 'Core language, OOP, data processing & scripting', 92, 'terminal', 1),
            ('programming', 'C / C++', 'Foundations & memory/pointers basics', 70, 'cpu', 2),

            # Data Science
            ('data_science', 'Data Analysis', 'Data cleaning, feature exploration & aggregation', 88, 'bar-chart-3', 1),
            ('data_science', 'Data Visualization', 'Interactive charts & exploratory data plotting', 86, 'pie-chart', 2),
            ('data_science', 'Pandas & NumPy', 'High-performance vector operations & tabular data manipulation', 85, 'table', 3),
            ('data_science', 'Matplotlib & Seaborn', 'Statistical visualizations & publication-ready plots', 82, 'line-chart', 4),
            ('data_science', 'OpenCV (cv2)', 'Computer vision, real-time image & video processing', 80, 'camera', 5),

            # Tools
            ('tools', 'Git & GitHub', 'Version control, branch management & open-source workflows', 88, 'git-branch', 1),
            ('tools', 'VS Code', 'Extensions, debugging & developer environment optimization', 92, 'monitor', 2),
            ('tools', 'Django Admin & SQLite', 'Database management & schema migrations', 85, 'database', 3),
        ]

        for cat, name, level, prof, icon, order in skills_data:
            Skill.objects.create(
                category=cat,
                name=name,
                level_note=level,
                proficiency=prof,
                icon_name=icon,
                is_featured=True,
                order=order,
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(skills_data)} skills"))

        # 4. Projects
        Project.objects.all().delete()
        projects_data = [
            {
                'title': "Face Recognition Attendance System",
                'category': "ai_ml",
                'tagline': "AI-powered biometric attendance tracker using OpenCV with desktop GUI",
                'description': (
                    "An AI-powered attendance tracking system utilizing OpenCV (cv2) for real-time facial feature extraction "
                    "and facial recognition, connected with an intuitive Tkinter desktop interface. Automates student/employee "
                    "attendance logging to eliminate manual paperwork and prevent proxy attendance."
                ),
                'extended_details': (
                    "### Architecture & Features:\n"
                    "- **Real-time Video Capture**: Processes live webcam feeds at high frame rates using OpenCV.\n"
                    "- **Facial Detection & Recognition**: Detects faces using Haar cascades / LBPH face recognizers, compares feature encodings against registered profiles.\n"
                    "- **Tkinter Graphical Interface**: Clean desktop user interface allowing administrators to register new users, train the face model, and monitor live attendance logs.\n"
                    "- **Automated Attendance Storage**: Instant logging of entry timestamps into a structured database / CSV output for audit-ready reporting.\n\n"
                    "### Tech Stack:\n"
                    "Python, OpenCV (cv2), Tkinter GUI, NumPy, Pillow, File I/O & SQLite."
                ),
                'tech_stack': "Python, OpenCV (cv2), Tkinter, NumPy, SQLite",
                'github_url': "https://github.com/makportx/face-recognition-attendance",
                'live_demo_url': "",
                'featured': True,
                'icon_name': "scan-face",
                'order': 1,
            },
            {
                'title': "Portfolio Website with AI Assistant",
                'category': "fullstack",
                'tagline': "Multi-page full-stack portfolio with an interactive contextual AI assistant",
                'description': (
                    "A dynamic, multi-page personal portfolio web application built using React, Node.js, and MongoDB. "
                    "Features an embedded interactive conversational AI assistant capable of answering visitor inquiries about skills, "
                    "experience, and projects in real time."
                ),
                'extended_details': (
                    "### Architecture & Features:\n"
                    "- **Modern Frontend**: Developed with React components, featuring responsive layouts, fluid transitions, and fast page navigation.\n"
                    "- **Backend API**: RESTful API endpoints powered by Node.js and Express for serving dynamic project data and handling contact inquiries.\n"
                    "- **MongoDB Database**: Document storage for portfolio items, user messages, and configuration.\n"
                    "- **Embedded AI Assistant**: Custom interactive conversational interface trained on resume context to answer visitor queries immediately without waiting for an email response.\n\n"
                    "### Tech Stack:\n"
                    "React, Node.js, Express, MongoDB, Tailwind CSS, JavaScript."
                ),
                'tech_stack': "React, Node.js, MongoDB, Express, Tailwind CSS",
                'github_url': "https://github.com/makportx/react-ai-portfolio",
                'live_demo_url': "",
                'featured': True,
                'icon_name': "bot",
                'order': 2,
            },
            {
                'title': "Data Dashboards (Practice Projects)",
                'category': "data_science",
                'tagline': "Interactive analytics dashboards built using Python, pandas, and matplotlib",
                'description': (
                    "A suite of exploratory data analysis (EDA) dashboards and visualizations built with Python, pandas, "
                    "and matplotlib. Synthesizes multi-dimensional datasets into digestible trends, distributions, and actionable insights."
                ),
                'extended_details': (
                    "### Architecture & Features:\n"
                    "- **Data Cleaning & Wrangling**: Automated preprocessing pipelines utilizing pandas for null handling, normalization, and aggregation.\n"
                    "- **Statistical Visualizations**: Custom plots including histograms, scatter matrices, heatmaps, and trend lines built using matplotlib and seaborn.\n"
                    "- **Key Metric Summaries**: Clear visual indicators for key performance indicators and statistical anomalies.\n"
                    "- **Notebook-to-Dashboard Workflow**: Organized Jupyter Notebook analyses transitioning into reusable visualization scripts.\n\n"
                    "### Tech Stack:\n"
                    "Python, Pandas, Matplotlib, Seaborn, Jupyter Notebooks."
                ),
                'tech_stack': "Python, Pandas, Matplotlib, Seaborn, Jupyter",
                'github_url': "https://github.com/makportx/python-data-dashboards",
                'live_demo_url': "",
                'featured': True,
                'icon_name': "bar-chart",
                'order': 3,
            },
            {
                'title': "Django Dynamic Portfolio & CMS Engine",
                'category': "fullstack",
                'tagline': "Production-ready Django portfolio engine with ORM models, Admin CMS & AI widget",
                'description': (
                    "The current robust portfolio platform built with Django 6 and modern UI principles. "
                    "Demonstrates Django Model-View-Template (MVT) architecture, automated data seeding, "
                    "database persistence for contact submissions, custom Django Admin management, and interactive APIs."
                ),
                'extended_details': (
                    "### Architecture & Features:\n"
                    "- **Django MVT Architecture**: Clean separation between ORM models, views, and server-rendered templates.\n"
                    "- **Full Django Admin Suite**: Enables effortless non-code content management for projects, skills, and contact messages.\n"
                    "- **Interactive Assistant Endpoint**: Integrated Django API endpoint processing inquiries and responding with resume data.\n"
                    "- **Printable Resume Generator**: Dedicated printer-optimized template allowing instant generation of clean PDF resumes.\n\n"
                    "### Tech Stack:\n"
                    "Django 6, Python 3, SQLite, Tailwind CSS, JavaScript."
                ),
                'tech_stack': "Django 6, Python 3, SQLite, Tailwind CSS, JavaScript",
                'github_url': "https://github.com/makportx/django-portfolio",
                'live_demo_url': "/",
                'featured': True,
                'icon_name': "layers",
                'order': 4,
            },
        ]

        for p_data in projects_data:
            Project.objects.create(
                title=p_data['title'],
                slug=slugify(p_data['title']),
                category=p_data['category'],
                tagline=p_data['tagline'],
                description=p_data['description'],
                extended_details=p_data['extended_details'],
                tech_stack=p_data['tech_stack'],
                github_url=p_data['github_url'],
                live_demo_url=p_data['live_demo_url'],
                featured=p_data['featured'],
                icon_name=p_data['icon_name'],
                order=p_data['order'],
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(projects_data)} projects"))

        # 5. Strengths
        Strength.objects.all().delete()
        strengths_data = [
            ("Strong problem-solving mindset", "Approaching complex software challenges with structured algorithmic thinking and systematic root-cause analysis.", "brain-circuit", 1),
            ("Quick adaptability to new technologies", "Rapidly picking up new frameworks, libraries, and languages to deliver modern solutions.", "zap", 2),
            ("Passion for merging design and functionality", "Crafting intuitive, delightful user experiences backed by robust, clean, maintainable code.", "sparkles", 3),
            ("Interest in both development & data insights", "Bridging the gap between software engineering and data science to build intelligent, data-driven applications.", "trending-up", 4),
        ]

        for title, desc, icon, order in strengths_data:
            Strength.objects.create(
                title=title,
                description=desc,
                icon_name=icon,
                order=order,
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(strengths_data)} strengths"))

        self.stdout.write(self.style.SUCCESS("\n🎉 Database successfully seeded with all resume information for ISREL!"))
