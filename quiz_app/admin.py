from django.contrib import admin
from .models import Quiz, Question, Answer, Attempt

from import_export import resources
from import_export.admin import ImportExportMixin

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Admin panelda savol qo'shish uchun qo'shimcha joy

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'deadline', 'max_attempts')  # Quizning asosiy ma'lumotlari
    search_fields = ('title',)  # Quiz nomi bo'yicha qidiruv
    list_filter = ('deadline',)  # Deadline bo'yicha filtrlash
    inlines = [QuestionInline]  # Quizga savollarni qo'shish

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'correct_option')  # Savol matni va tegishli quiz
    search_fields = ('text', 'quiz__title')  # Savol matni va quiz nomi bo'yicha qidiruv
    list_filter = ('quiz',)  # Quiz bo'yicha filtrlash

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'selected_option', 'is_correct')  # Javob ma'lumotlari
    list_filter = ('is_correct', 'question__quiz')  # To'g'ri/noto'g'ri javoblar va quiz bo'yicha filtrlash
    search_fields = ('student__full_name', 'question__text')  # Talaba ismi va savol matni bo'yicha qidiruv

# Attempt uchun Resource klassi
class AttemptResource(resources.ModelResource):
    class Meta:
        model = Attempt
        fields = ('id', 'student__full_name', 'quiz__title', 'score', 'attempt_date')  # Faqat kerakli maydonlar
        export_order = ('id', 'student__full_name', 'quiz__title', 'score', 'attempt_date')

# Attempt admin
@admin.register(Attempt)
class AttemptAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = AttemptResource
    list_display = ('student', 'quiz', 'score', 'attempt_date')
    search_fields = ('student__full_name', 'quiz__title')
    list_filter = ('quiz', 'attempt_date')