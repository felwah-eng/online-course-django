from django.contrib import admin
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# Seven imported model classes: User, Course, Lesson, Question, Choice, Submission, Enrollment.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'course', 'grade')
    list_filter = ('course',)
    search_fields = ('question_text',)
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    inlines = [QuestionInline]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'score', 'total', 'submitted_at')
    readonly_fields = ('enrollment', 'score', 'total', 'submitted_at')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Enrollment)
# Django's built-in Authentication and Authorization registers Users and Groups.
admin.site.site_header = 'Online Course Administration'
admin.site.site_title = 'Online Course Admin'
