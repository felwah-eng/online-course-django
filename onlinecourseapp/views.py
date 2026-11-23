from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Course, Enrollment, Submission


def course_list(request):
    return render(request, 'onlinecourseapp/course_list.html', {
        'courses': Course.objects.all().order_by('id')
    })


def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related('lessons', 'questions__choices'), pk=course_id)
    return render(request, 'onlinecourseapp/course_details_bootstrap.html', {'course': course})


@login_required(login_url='/admin/login/')
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    questions = list(course.questions.prefetch_related('choices'))
    if not questions:
        messages.error(request, 'This course does not have an exam yet.')
        return redirect('onlinecourseapp:course_details', course_id=course.id)

    score = 0
    total = sum(question.grade for question in questions)
    for question in questions:
        selected = set(request.POST.getlist(f'question_{question.id}'))
        correct = {str(choice.pk) for choice in question.choices.all() if choice.is_correct}
        if selected == correct:
            score += question.grade

    submission = Submission.objects.create(enrollment=enrollment, score=score, total=total)
    return redirect('onlinecourseapp:show_exam_result', course_id=course.id, submission_id=submission.id)


@login_required(login_url='/admin/login/')
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related('enrollment__course'),
        pk=submission_id, enrollment__course_id=course_id, enrollment__user=request.user,
    )
    percentage = round(100 * submission.score / submission.total) if submission.total else 0
    return render(request, 'onlinecourseapp/exam_result.html', {
        'course': submission.enrollment.course,
        'submission': submission,
        'percentage': percentage,
        'passed': percentage >= 70,
    })
