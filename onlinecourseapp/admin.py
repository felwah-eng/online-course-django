
from django.contrib import admin
from django.contrib.auth.models import User

from .models import (
    Choice,
    Course,
    Enrollment,
    Instructor,
    Learner,
    Lesson,
    Question,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "grade")
    list_filter = ("course",)
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    inlines = [QuestionInline]


class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")
    list_filter = ("full_time",)
    search_fields = ("user__username",)


class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation", "social_link")
    list_filter = ("occupation",)
    search_fields = ("user__username",)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrolled_at")
    list_filter = ("course",)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "score", "total", "submitted_at")
    readonly_fields = (
        "enrollment",
        "score",
        "total",
        "submitted_at",
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)

# User and Group are registered by Django's built-in admin.
admin.site.site_header = "Online Course Administration"
admin.site.site_title = "Online Course Admin"

