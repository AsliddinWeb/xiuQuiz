from django.db import models

class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name="Guruh nomi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

class Student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Guruhi")
    full_name = models.CharField(max_length=255, verbose_name="Ism familiya")

    def __str__(self):
        return f"{self.full_name} | {self.group}"

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"
