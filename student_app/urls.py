from django.urls import path
from . import views

urlpatterns = [
    path('filter/<int:group_id>/', views.filter_students, name='filter_students'),
]
