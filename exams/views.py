from datetime import datetime as dt, timedelta, date
from django.shortcuts import render
from .models import Facoltà, Exam, DateExam
from django.views import generic
import calendar
import threading
from .utils import Calendar
from django.core.management import call_command
from django.utils.safestring import mark_safe
from exams.HTMLParsing import *
from django.http import HttpResponseRedirect
from dateutil.relativedelta import relativedelta

# Create your views here.
global che, d
che =[]
d = ""

def getChe():
    return che
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
        global ciao, d
        context = super().get_context_data(**kwargs)
        if not d:
            d = get_date(self.request.GET.get('month', None))
        checklist = getChe()
        cal = Calendar(d.year, d.month, self.kwargs['id'], checklist)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['facolta'] = Facoltà.objects.get(id=self.kwargs['id'])
        return context
    def post(self, request, *args, **kwargs):
        global che, d
        stato = self.request.POST.get('stato')
        data = self.request.POST.get('data')
        if stato == 'next':
            d += relativedelta(months=1)
            return HttpResponseRedirect('/exams/'+str(kwargs['id'])+'?'+next_month(d))
        elif stato == 'prev':
            d += relativedelta(months=-1)
            return HttpResponseRedirect('/exams/' + str(kwargs['id']) + '?' + prev_month(d))
        else:
            if data is not None:
                d = dt.strptime(data, '%Y-%m-%d').date()
            checklist = self.request.POST.getlist('lis[]')
            checklist = [int(ch) for ch in checklist]
            che = checklist
            return HttpResponseRedirect('/exams/'+str(kwargs['id'])+'?month='+str(d.year)+'-'+str(d.month))



def createFacoulty():
    courses = get_corso_di_studio_ingegneria()
    durata = getDurata()
    for i in range(1, len(courses)):
        Facoltà.objects.create(nome=courses[i].text,anno=durata[i-1])

def createDateExam(facoltà):
    date = getDateExam()
    for d in date:
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
    return ret





def restart():

    threading.Timer(86400.0, restart).start()
    call_command('flush', '--no-input')
    createFacoulty()
    for facoltà in Facoltà.objects.all():
        if getCod(facoltà) is not None:
            today = datetime.date.today()
            year = today.year
            year -= 1
            while year >= 2019:
                ret = connectToEsse3Page(getCod(facoltà), year)
                year -= 1
                createExam(nome=getExam(), anno=getAnno(), semestre=getSemestre(), crediti=getCrediti(), facoltà=facoltà)
                createDateExam(facoltà)
        else:
            continue

#restart()


def exams(request):

    facoltà = list(Facoltà.objects.all())

    global che, d
    d = ""
    che = []
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
    return render(request, 'exams/facolt.html', context=context)




