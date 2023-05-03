from django.contrib.auth.models import User
from django.core.management.color import no_style
from django.db import connection
from datetime import datetime as dt, timedelta, date
from django.shortcuts import render
from .models import Facoltà, Exam, DateExam
from django.views import generic
import calendar
from .utils import Calendar
from django.utils.safestring import mark_safe
from exams.HTMLParsing import *
from django.http import HttpResponseRedirect

# Create your views here.

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return dt.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(generic.ListView):
    model = DateExam
    template_name = 'exams/calendar.html'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        cal.getI(self.kwargs['i'], self.kwargs['id'])
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['id'] = self.kwargs['id']
        context['i'] = self.kwargs['i']
        return context





def createFacoulty():
    courses = get_corso_di_studio_ingegneria()
    durata = getDurata()
    for i in range(1, len(courses)):
        Facoltà.objects.create(nome=courses[i].text,anno=durata[i-1])

def createDateExam(facoltà):
    date = getDateExam()
    for d in date:
        print(d["exam"])
        DateExam.objects.get_or_create(data=d["data"], exam=Exam.objects.get(nome=d["exam"], facoltà=facoltà))



def createExam(nome,anno,semestre,crediti,facoltà):
    for i in range(len(anno)):

        Exam.objects.get_or_create(nome=nome[i], anno=anno[i], semestre=semestre[i], crediti=crediti[i], facoltà=facoltà)


def getCod(facoltà):
    temp = facoltà.nome
    for e in temp.split('] '):
        break
    for ret in e.split('['):
        continue
    print(ret)
    return ret



import threading

def restart():

    threading.Timer(86400.0, restart).start()

    fac = Facoltà.objects.all()
    for fa in fac:
        fa.delete()

    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Facoltà, Exam, DateExam])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)

    createFacoulty()
    for facoltà in Facoltà.objects.all():
        if getCod(facoltà) is not None:
            #connectToEsse3Page(getCod(facoltà))
            createExam(nome=getExam(), anno=getAnno(), semestre=getSemestre(), crediti=getCrediti(), facoltà=facoltà)
            createDateExam(facoltà)
        else:
            continue

restart()


def exams(request):

    facoltà = list(Facoltà.objects.all())

    dat = list(DateExam.objects.values_list('exam__facoltà__nome', flat=True))

    i = 0

    for fac in Facoltà.objects.all():
        if fac.nome not in dat:
            facoltà.pop(i)
        else:
            i += 1

    context = {
        "facoltà": facoltà,
    }
    return render(request, 'exams/tutorial_bootstrap.html', context=context)


def choice(request,id):
    facoltà = Facoltà.objects.get(id=id)
    global i
    i=id
    context = {
        "facoltà": facoltà,
    }

    return render(request, 'exams/choices.html', context=context)



print(dateExam)


def deleteExams(request, id):

    print("QUI")
    fac = Facoltà.objects.get(id=id)
    ex = Exam.objects.all()
    for e in ex:
        if e.facoltà == fac:
            e.delete()


    return HttpResponseRedirect('/exams/'+str(fac.id))


def deleteDateExams(request, id):

    fac = Facoltà.objects.get(id=id)

    dex = DateExam.objects.all()
    for de in dex:
        if de.exam.facoltà == fac:
            de.delete()


    return HttpResponseRedirect('/exams/'+str(fac.id))





def f(request, id, i):
    global ids
    a = 0
    s = 0
    ex = []
    facoltà = Facoltà.objects.get(id=id)

    if i == 1:
        a = 1
        s = 1
    elif i == 2:
        a = 1
        s = 2
    elif i == 3:
        a = 2
        s = 1
    elif i == 4:
        a = 2
        s = 2
    elif i == 5:
        a = 3
        s = 1
    else:
        a = 3
        s = 2

    date = DateExam.objects.all().order_by('data')
    e = Exam.objects.all()
    for el in e:
        if el.facoltà.id == facoltà.id:
            ex.append(el)

    context = {
        "facoltà": facoltà,
        "exam": ex,
        "date": date,
        "semestre": s,
        "anno": a,
    }
    return render(request, "exams/facoltà.html", context=context)

