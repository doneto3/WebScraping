from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Facoltà, Exam, DateExam
from exams.HTMLParsing import *
from django.http import HttpResponseRedirect

# Create your views here.





def createFacoulty():
    courses = get_corso_di_studio_ingegneria()
    durata = getDurata()
    for i in range(1, len(courses)):
        Facoltà.objects.get_or_create(nome=courses[i].text,anno=durata[i-1])

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

createFacoulty()

for facoltà in Facoltà.objects.all():
    connectToEsse3Page(getCod(facoltà))
    createExam(nome=getExam(), anno=getAnno(), semestre=getSemestre(), crediti=getCrediti(), facoltà=facoltà)
    createDateExam(facoltà)


def exams(request):
    facoltà = Facoltà.objects.all()
    context = {
        "facoltà": facoltà,
    }
    return render(request, 'exams/tutorial_bootstrap.html', context=context)


def choice(request,id):
    facoltà = Facoltà.objects.get(id=id)

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

