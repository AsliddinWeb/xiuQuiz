from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('result/<int:quiz_id>/<int:student_id>/', views.quiz_result, name='quiz_result'),  # Natijalarni ko'rish
    path('logout/', views.logout, name='logout'),

    path('admin-results/', views.quiz_results_admin, name='quiz_results_admin'),
    path("student-create/", views.student_import, name="student_import"),
]
