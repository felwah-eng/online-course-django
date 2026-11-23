from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Question(models.Model):
course = models.ForeignKey(
Course,
on_delete=models.CASCADE,
related_name='questions'
)
question_text = models.CharField(max_length=500)
grade = models.PositiveIntegerField(default=1)

def is_get_score(self, selected_choices=None):
    if selected_choices is None:
        return 0

    selected_ids = {
        choice.id if isinstance(choice, Choice) else int(choice)
        for choice in selected_choices
    }

    correct_ids = set(
        self.choices.filter(is_correct=True).values_list('id', flat=True)
    )

    return self.grade if correct_ids and selected_ids == correct_ids else 0

def __str__(self):
    return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    choices = models.ManyToManyField('Choice', related_name='submissions', blank=True)
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.enrollment} — {self.score}/{self.total}'


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'course'], name='unique_course_enrollment')]

    def __str__(self):
        return f'{self.user.username} — {self.course.name}'
