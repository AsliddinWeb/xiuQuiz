from django.http import JsonResponse
from .models import Student

def filter_students(request, group_id):
    students = Student.objects.filter(group_id=group_id).values('id', 'full_name')
    return JsonResponse({'students': list(students)})

