from django.core.management.base import BaseCommand
from django.db import transaction
from onlinecourseapp.models import Course, Lesson, Question, Choice


class Command(BaseCommand):
    help = 'Create a demonstration course, lessons, questions and choices'

    @transaction.atomic
    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(name='Introduction to Django', defaults={
            'description': 'Learn the basics of Django web development and test your knowledge.'
        })
        for order, (title, content) in enumerate([
            ('Getting Started', 'Django is a Python framework for building database-driven web apps.'),
            ('Django Models', 'Models describe structured data and relationships in a database.'),
            ('Views and Templates', 'Views prepare responses, and templates generate HTML pages.'),
        ], 1):
            Lesson.objects.get_or_create(course=course, order=order, defaults={'title': title, 'content': content})
        data = [
            ('Which programming language is Django written in?', [('Python', True), ('JavaScript', False), ('Ruby', False)]),
            ('Which Django file typically defines database tables?', [('models.py', True), ('views.py', False), ('urls.py', False)]),
            ('Which command applies database migrations?', [('python manage.py migrate', True), ('python manage.py runserver', False)]),
        ]
        for prompt, answers in data:
            question, created = Question.objects.get_or_create(course=course, question_text=prompt, defaults={'grade': 1})
            if created:
                for answer, correct in answers:
                    Choice.objects.create(question=question, choice_text=answer, is_correct=correct)
        self.stdout.write(self.style.SUCCESS('Demo course ready: http://127.0.0.1:8000/'))
