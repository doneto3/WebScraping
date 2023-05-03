from django.urls import path, re_path
from . import views
from .models import Facoltà

urlpatterns = [
    path('', views.exams, name='home'),
    path('<int:id>', views.choice, name='choice'),
    path('<int:id>/delete/', views.deleteExams, name='delete'),
    path('<int:id>/deleteExam/', views.deleteDateExams, name='delete'),
    path('<int:id>/<int:i>', views.CalendarView.as_view(), name='facoltà'),
]