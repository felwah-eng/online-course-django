
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Course, Enrollment, Submission


def course_list(request):
    courses = Course.objects.all().order_by("id")
    return render(
        request,
        "onlinecourseapp/course_list.html",
        {"courses": courses},
    )


def course_details(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related(
            "lessons",
            "questions__choices",
        ),
        pk=course_id,
    )

    return render(
        request,
        "onlinecourseapp/course_details_bootstrap.html",
        {"course": course},
    )


@login_required(login_url="/admin/login/")
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
    )

    questions = list(
        course.questions.prefetch_related("choices")
    )

    if not questions:
        messages.error(
            request,
            "This course does not have an exam yet.",
        )
        return redirect(
            "onlinecourseapp:course_details",
            course_id=course.id,
        )

    selected_choices = []
    score = 0
    total = sum(question.grade for question in questions)

    for question in questions:
        selected_ids = set(
            request.POST.getlist(
                f"question_{question.id}"
            )
        )

        choices = list(question.choices.all())

        valid_choices = [
            choice for choice in choices
            if str(choice.pk) in selected_ids
        ]

        selected_choices.extend(valid_choices)

        score += question.is_get_score(valid_choices)

    submission = Submission.objects.create(
        enrollment=enrollment,
        score=score,
        total=total,
    )

    submission.choices.set(selected_choices)

    return redirect(
        "onlinecourseapp:show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required(login_url="/admin/login/")
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__course=course,
        enrollment__user=request.user,
    )

    selected_ids = set(
        submission.choices.values_list("pk", flat=True)
    )

    questions = list(
        course.questions.prefetch_related("choices")
    )

    total = sum(question.grade for question in questions)
    grade = 0

    for question in questions:
        selected_for_question = [
            choice.pk
            for choice in question.choices.all()
            if choice.pk in selected_ids
        ]

        grade += question.is_get_score(
            selected_for_question
        )

    percentage = round(100 * grade / total) if total else 0

    submission.score = grade
    submission.total = total
    submission.save(
        update_fields=["score", "total"]
    )

    context = {
        "course": course,
        "submission": submission,
        "selected_ids": selected_ids,
        "grade": grade,
        "total": total,
        "percentage": percentage,
        "passed": percentage >= 70,
    }

    return render(
        request,
        "onlinecourseapp/exam_result_bootstrap.html",
        context,
    )
