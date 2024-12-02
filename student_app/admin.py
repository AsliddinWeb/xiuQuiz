from django.contrib import admin
from .models import Group, Student

from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Guruh nomini ko'rsatadi
    search_fields = ('title',)  # Guruh nomi bo'yicha qidiruv

# Student uchun Resource klassi
class StudentResource(resources.ModelResource):
    group__title = Field(attribute='group', column_name='group__title')

    class Meta:
        model = Student
        import_id_fields = []  # Importda ID ustunini ishlatmaymiz
        exclude = ('id',)  # ID ustunini butunlay chiqaramiz
        fields = ('full_name', 'group__title')  # Kerakli ustunlar
        export_order = ('full_name', 'group__title')

    def before_import_row(self, row, **kwargs):
        """
        Group obyektini avtomatik topish yoki yaratish
        """
        group_title = row.get('group__title')  # Fayldagi group__title ustuni
        if group_title:
            # Group obyektini yaratish yoki topish
            group, created = Group.objects.get_or_create(title=group_title)
            row['group'] = group  # Group obyekti instansiyasi

# Student admin
@admin.register(Student)
class StudentAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = StudentResource
    list_display = ('full_name', 'group')
    search_fields = ('full_name',)
    list_filter = ('group',)