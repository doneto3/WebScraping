from django.urls import path, re_path
from . import views
from .models import Facoltà

urlpatterns = [
    path('', views.exams, name='home'),
    path('<int:id>', views.CalendarView.as_view(), name='facoltà'),
    path('<int:id>/aggiorna', views.aggiornaAule, name='aggiornaAule'),
]