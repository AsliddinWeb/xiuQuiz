from django.db import models
from student_app.models import Student

class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name="Quiz nomi")
    description = models.TextField(verbose_name="Tavsif", blank=True, null=True)
    deadline = models.DateTimeField(verbose_name="Oxirgi muddat")
    max_attempts = models.IntegerField(verbose_name="Maksimal urinishlar", default=1)
    points_per_question = models.FloatField(verbose_name="Har bir savol uchun ball", default=1.0)  # Ball
    question_count = models.IntegerField(verbose_name="Savollar soni", default=5)  # Savollar soni

    def __str__(self):
        return self.title

    def total_points(self):
        """Quiz bo'yicha umumiy ballni qaytaradi"""
        return self.points_per_question * self.question_count

    class Meta:
        verbose_name_plural = "Testlar boshqaruvi"
        verbose_name = "Test"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Quiz")
    text = models.TextField(verbose_name="Savol matni")
    option1 = models.CharField(max_length=255, verbose_name="Variant 1")
    option2 = models.CharField(max_length=255, verbose_name="Variant 2")
    option3 = models.CharField(max_length=255, verbose_name="Variant 3")
    option4 = models.CharField(max_length=255, verbose_name="Variant 4")
    correct_option = models.IntegerField(verbose_name="To'g'ri javob (1-4)")

    def __str__(self):
        return f"{self.text[:50]}... ({self.quiz.title})"

    class Meta:
        verbose_name_plural = "Savollar"
        verbose_name = "Savol"


class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Talaba")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Savol")
    selected_option = models.IntegerField(verbose_name="Tanlangan javob")
    is_correct = models.BooleanField(verbose_name="To'g'ri yoki noto'g'ri", default=False)

    def __str__(self):
        return f"{self.student.full_name} - {self.question.text[:30]}"

    class Meta:
        verbose_name_plural = "Javoblar"
        verbose_name = "Javob"


class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Talaba")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Quiz")
    score = models.FloatField(verbose_name="Natija", default=0)
    attempt_date = models.DateTimeField(auto_now_add=True, verbose_name="Urinish sanasi")

    def __str__(self):
        return f"{self.student.full_name} - {self.quiz.title} ({self.score})"

    class Meta:
        verbose_name_plural = "Natijalar"
        verbose_name = "Natija"
