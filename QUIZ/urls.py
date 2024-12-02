from django.contrib import admin
from django.urls import path, include

# Admin sarlavha va matnlarini o'zgartirish
admin.site.site_header = "XIU Test Tizimi"
admin.site.site_title = "XIU Test Tizimi"
admin.site.index_title = "Testlar va Talabalar Boshqaruvi"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz_app.urls')),
    path('students/', include('student_app.urls')),
]
