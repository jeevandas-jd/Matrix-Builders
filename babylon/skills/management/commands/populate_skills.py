from django.core.management.base import BaseCommand
from skills.models import Skill

class Command(BaseCommand):
    help = 'Populate the Skill model with initial data'

    def handle(self, *args, **kwargs):
        skills_data = [
            {'name': 'Python Programming', 'description': 'Learn the basics of Python programming.'},
            {'name': 'Web Development', 'description': 'Build websites using HTML, CSS, and JavaScript.'},
            {'name': 'Data Analysis', 'description': 'Analyze data using various tools and techniques.'},
            {'name': 'Graphic Design', 'description': 'Create stunning graphics and designs.'},
            {'name': 'Digital Marketing', 'description': 'Promote products and services online.'},
            # Add more skills as needed
        ]

        for skill in skills_data:
            obj, created = Skill.objects.get_or_create(**skill)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created skill: {skill["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skill already exists: {skill["name"]}'))
