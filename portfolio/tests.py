import io
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from portfolio.models import Profile, Education, Skill, Project, Strength, ContactMessage


class PortfolioTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('seed_portfolio', stdout=io.StringIO())

    def test_seed_portfolio_created_records(self):
        """Verify that seed_portfolio populates all models with Isrel's resume info."""
        profile = Profile.objects.first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.name, "ISREL")
        self.assertEqual(profile.email, "makportx@gmail.com")
        self.assertEqual(profile.github, "https://github.com/makportx")
        self.assertIn("Chennai", profile.location)

        self.assertTrue(Education.objects.filter(institution__icontains="SRM").exists())
        self.assertTrue(Skill.objects.filter(name="Django").exists())
        self.assertTrue(Skill.objects.filter(name="Python").exists())
        self.assertTrue(Project.objects.filter(title__icontains="Face Recognition").exists())
        self.assertTrue(Strength.objects.filter(title__icontains="problem-solving").exists())

    def test_home_view(self):
        """Test the home landing page loads correctly."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ISREL")
        self.assertContains(response, "Aspiring Web Developer")
        self.assertContains(response, 'id="about"')
        self.assertContains(response, "About Me")
        self.assertContains(response, "SRM Institute of Science and Technology")
        self.assertContains(response, "Face Recognition Attendance System")

    def test_project_detail_view(self):
        """Test that project detail pages render correctly."""
        project = Project.objects.first()
        response = self.client.get(reverse('project_detail', kwargs={'slug': project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, project.title)
        self.assertTemplateUsed(response, 'portfolio/project_detail.html')

    def test_resume_view(self):
        """Test that the printable resume page loads."""
        response = self.client.get(reverse('resume'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "makportx@gmail.com")
        self.assertContains(response, "Expected Graduation: May 2029")
        self.assertTemplateUsed(response, 'portfolio/resume.html')

    def test_contact_form_submission(self):
        """Test submitting the contact form saves to database."""
        initial_count = ContactMessage.objects.count()
        response = self.client.post(reverse('home'), {
            'name': 'Recruiter Jane',
            'email': 'jane@techcorp.com',
            'subject': 'Exciting Full-Stack Internship Opportunity',
            'message': 'Hi Isrel, we were impressed by your projects and would love to chat!',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), initial_count + 1)
        new_msg = ContactMessage.objects.latest('created_at')
        self.assertEqual(new_msg.name, 'Recruiter Jane')
        self.assertEqual(new_msg.email, 'jane@techcorp.com')
        self.assertFalse(new_msg.is_read)

    def test_ai_assistant_api(self):
        """Test AI resume assistant API endpoint responses."""
        # Query about skills
        response = self.client.post(
            reverse('ai_assistant_api'),
            data=json.dumps({'query': 'what skills do you know?'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('Python', data['response'])
        self.assertIn('Django', data['response'])

        # Query about education
        response = self.client.post(
            reverse('ai_assistant_api'),
            data=json.dumps({'query': 'where did you study?'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('SRM', data['response'])
