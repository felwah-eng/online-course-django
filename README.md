# Online Course App — Django

An editable Django online-learning application with course and lesson detail pages, an admin dashboard, a multiple-choice exam, and a results page.

## Included grading artifacts

1. `onlinecourseapp/models.py`: `Question`, `Choice`, `Submission` plus `Course`, `Lesson` and `Enrollment`.
2. `onlinecourseapp/admin.py`: imports seven model classes (`User`, `Course`, `Lesson`, `Question`, `Choice`, `Submission`, `Enrollment`) and implements `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, `LessonAdmin`.
3. Screenshot `03-admin-site`: **capture this from your running app**, showing **Authentication and Authorization** and **Onlinecourseapp**.
4. `onlinecourseapp/templates/onlinecourseapp/course_details_bootstrap.html`: Bootstrap course page with related lessons and exam form.
5. `onlinecourseapp/views.py`: `submit` and `show_exam_result` views.
6. `onlinecourseapp/urls.py`: routes for exam submit and results, with the project's root routing in `onlinecourse/urls.py`.
7. Screenshot `07-final`: **capture this from your running app** after a successful exam attempt, showing **Congratulations!**, score and result.

## Run locally (requires Python 3.10+)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` and log in with your superuser to capture `03-admin-site`.
For `07-final`, log in, visit `http://127.0.0.1:8000/`, open **Introduction to Django**, select the correct choices, submit, and capture the **Congratulations!** screen.

**Do not upload screenshots of a simulated admin page or an unexecuted exam.** Both rubric screenshots should come from your own running application.

Security: the project uses a development-only secret by default. Configure proper environment secrets and hosts before any real deployment. Do not upload `db.sqlite3` or secrets to GitHub.
