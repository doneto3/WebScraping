from django.contrib import admin
from .models import Facoltà, Exam, DateExam, Aula
# Register your models here.

admin.site.register(Facoltà)
admin.site.register(Exam)
admin.site.register(DateExam)
admin.site.register(Aula)