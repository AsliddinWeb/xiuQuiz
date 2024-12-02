import random
import pandas as pd

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .models import Quiz, Question, Answer, Attempt
from student_app.models import Student, Group


def home(request):
    """
    Bosh sahifa: Guruh va talabani tanlash uchun forma.
    Tanlangan talaba sessiyada saqlanadi.
    """
    from student_app.forms import StudentSelectionForm  # Import form dynamically to avoid circular import
    group_id = request.POST.get('group')  # Guruh ID'sini olish
    form = StudentSelectionForm(group_id=group_id)  # Dinamik talaba filtrlash

    if request.method == 'POST':
        student_id = request.POST.get('student')
        if group_id and student_id:
            # Sessiyaga talaba ID'sini saqlash
            request.session['student_id'] = student_id
            return redirect('quiz_list')

    return render(request, 'quiz_app/home.html', {'form': form})


def quiz_list(request):
    """
    Talabalar uchun mavjud testlar ro'yxatini ko'rsatadi.
    Har bir test uchun urinishlar soni hisoblanadi.
    """
    # Sessiyadan talabani olish
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('home')  # Talaba aniqlanmasa, bosh sahifaga qaytaradi

    student = Student.objects.get(id=student_id)
    quizzes = Quiz.objects.all()

    # Har bir test uchun urinishlar sonini hisoblash
    for quiz in quizzes:
        quiz.attempt_count = Attempt.objects.filter(student=student, quiz=quiz).count()

    return render(request, 'quiz_app/quiz_list.html', {'quizzes': quizzes, 'student': student})


def quiz_detail(request, quiz_id):
    """
    Quiz tafsilotlari va tasodifiy savollar.
    """
    # Sessiyadan talabani olish
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('home')

    student = get_object_or_404(Student, id=student_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Maksimal urinish soni tekshiruvi
    if Attempt.objects.filter(student=student, quiz=quiz).count() >= quiz.max_attempts:
        messages.error(request, "Maksimal urinish soniga yetdingiz!")
        return redirect('quiz_list')

    # Quiz savollarini tasodifiy olish
    all_questions = list(quiz.questions.all())
    random_questions = random.sample(all_questions, min(len(all_questions), quiz.question_count))

    if request.method == 'POST':
        score = 0
        points_per_question = quiz.points_per_question
        for question in random_questions:
            selected_option = int(request.POST.get(f'question_{question.id}', 0))
            is_correct = selected_option == question.correct_option
            score += points_per_question if is_correct else 0
            # Javoblarni saqlash
            Answer.objects.create(
                student=student,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct,
            )

        # Urinishni saqlash
        Attempt.objects.create(student=student, quiz=quiz, score=score)
        return redirect('quiz_result', quiz_id=quiz.id, student_id=student.id)

    return render(request, 'quiz_app/quiz_detail.html', {
        'quiz': quiz,
        'questions': random_questions,
    })


def quiz_result(request, quiz_id, student_id):
    """
    Test natijalarini ko'rsatadi.
    """
    student = get_object_or_404(Student, id=student_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Oxirgi urinishni olish
    attempt = Attempt.objects.filter(student=student, quiz=quiz).last()

    return render(request, 'quiz_app/quiz_result.html', {
        'quiz': quiz,
        'student': student,
        'attempt': attempt,
        'total_points': quiz.total_points(),
    })



def logout(request):
    """
    Sessiyani tozalash va bosh sahifaga qaytarish.
    """
    request.session.flush()  # Barcha sessiya ma'lumotlarini o'chirish
    return redirect('home')

@staff_member_required
def quiz_results_admin(request):
    """
    Superadminlar uchun har bir talabaning oxirgi urinish natijalarini ko'rsatadigan sahifa.
    """
    quizzes = Quiz.objects.all()
    selected_quiz = None
    results = []

    if request.method == 'POST' and 'download_excel' in request.POST:
        quiz_id = request.POST.get('quiz')
        selected_quiz = get_object_or_404(Quiz, id=quiz_id)

        # Har bir talabaning oxirgi urinishini olish
        latest_attempts = (
            Attempt.objects.filter(quiz=selected_quiz)
            .values('student')
            .annotate(latest_date=Max('attempt_date'))
        )

        results = Attempt.objects.filter(
            quiz=selected_quiz,
            attempt_date__in=[item['latest_date'] for item in latest_attempts]
        )

        # Excelga eksport qilish
        data = [
            {
                "Talaba": result.student.full_name,
                "Ball": result.score,
                "Sana": result.attempt_date.replace(tzinfo=None),  # Timezone'ni olib tashlash
            }
            for result in results
        ]

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{selected_quiz.title}_results.xlsx"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Results")

        return response

    elif request.method == 'POST':
        quiz_id = request.POST.get('quiz')
        selected_quiz = get_object_or_404(Quiz, id=quiz_id)

        latest_attempts = (
            Attempt.objects.filter(quiz=selected_quiz)
            .values('student')
            .annotate(latest_date=Max('attempt_date'))
        )

        results = Attempt.objects.filter(
            quiz=selected_quiz,
            attempt_date__in=[item['latest_date'] for item in latest_attempts]
        )

    return render(request, 'quiz_app/quiz_results_admin.html', {
        'quizzes': quizzes,
        'selected_quiz': selected_quiz,
        'results': results,
    })

def student_import(request):
    """
    Adminlar uchun talabalarning Excel faylini yuklash orqali yaratish.
    """
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        try:
            # Excel faylni pandas yordamida o'qish
            data = pd.read_excel(file)

            # Fayldagi ustun nomlari mosligini tekshirish
            required_columns = ["To‘liq ismi", "Guruh"]
            if not all(column in data.columns for column in required_columns):
                messages.error(request, "Excel faylda kerakli ustunlar mavjud emas.")
                return redirect("student_import")

            # Har bir qatorni qayta ishlash
            for _, row in data.iterrows():
                full_name = row["To‘liq ismi"]
                group_title = row["Guruh"]

                # Guruhni yaratish yoki topish
                group, created = Group.objects.get_or_create(title=group_title)

                # Talabani yaratish
                Student.objects.get_or_create(full_name=full_name, group=group)

            messages.success(request, "Talabalar muvaffaqiyatli import qilindi!")
            return redirect("student_import")

        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return redirect("student_import")

    return render(request, "student_app/student_import.html")