from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import datetime
from selenium.common.exceptions import NoSuchElementException
from .models import Facoltà, Exam, DateExam


global cds_id, cds, calendar_id, calendar_list, esame, iscr, turno, tipo, docente, num_iscr
anno = []
semestre = []
crediti = []
exam = []
examNull = []
durata = []
dateExam = []

def setZero():
    global anno, semestre, crediti, exam, durata, dateExam, examNull
    anno = []
    semestre = []
    crediti = []
    exam = []
    durata = []
    dateExam = []
    examNull = []

calendars = {}

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True




def createCourseString(cod):
    for i in range(1,len(options)):
        if cod in options[i].text:
            mat = options[i].text[9:]
            break
    al = cod[3:]
    if int(al) >= 250:
        al = '[LM]'

    else:
        al = '[LT]'

    ret = al+'\u00A0​' + mat + ' - '+cod
    return ret


def getAnno():
    return anno
def getCrediti():
    return crediti
def getExam():
    return exam
def getSemestre():
    return semestre

def getDurata():
    return durata

def getDateExam():
    return dateExam

def apostrofoString(e):
    ret = []
    for temp in e.split('\''):
        ret.append(temp)
    return ret[0]+'&apos;'+ret[1]

def connectToEsse3Page(cod, yea):
    global anno, semestre, crediti, exam, durata, dateExam, examNull
    cds_id = getValue(cod)
    setZero()
    if cds_id is None:
        return
    url = 'https://www.esse3.unimore.it/Guide/PaginaListaAppelli.do?FAC_ID=10005&CDS_ID=' + cds_id + '&AD_ID=X&DOCENTE_ID=X&DATA_ESA=&actionBar1=1'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver = ChromeDriverManager().install()
    driver = Chrome(service=Service(chrome_driver), options=chrome_options)
    exam_table = soup.find(attrs={"class": "table-1-body"})
    table_elem = exam_table.find_all("tr")


    for i in range(len(table_elem)):
        tmp = {}
        table_item = table_elem[i].find_all("td")
        count = len(table_item)
        if count == 6:
            esame = table_item[0].text
            iscr = table_item[1].text
            turno = table_item[2].text
            tipo = table_item[3].text
            if tipo == "":
                tipo = "Sconosciuto"
            docente = table_item[4].text.replace("\n", " ").strip()
            if docente == "":
                docente = "Sconosciuto"
            num_iscr = table_item[5].text
            tmp["iscr"] = iscr
        else:
            turno = table_item[0].text
            tipo = table_item[1].text
            if tipo == "":
                tipo = "Sconosciuto"
            docente = table_item[2].text.replace("\n", " ").strip()
            if docente == "":
                docente = "Sconosciuto"
            num_iscr = table_item[3].text



        summary = esame
        description = "Periodo Iscrizioni: " + iscr + "\n" + "Tipo: " + tipo + "\n" + "Docente/i: " + docente + "\n" + "Numero iscritti: " + num_iscr
        day = int(turno[0:2])
        month = int(turno[3:5])
        year = int(turno[6:10])
        try:
            hour = turno[13:15]
            minute = turno[16:18]
            time.sleep(0.005)
        except:
            hour = "09"
            minute = "00"
            time.sleep(0.005)

        print(summary + '\n' + description + '\n' + str(day) + '/' + str(month) + '/' + str(year) + ' '
              + hour + ':' + minute + '\n')

        for e in summary.split('] '):
            continue
        print(i)
        if '\'' in e:
            e = apostrofoString(e)



        tmp["exam"] = e
        tmp["tipo"] = tipo
        tmp["docente"] = docente
        tmp["num_iscr"] = num_iscr
        try:
            tmp["data"] = datetime.datetime.strptime(str(day) + '/' + str(month) + '/' + str(year) + ' '
                                                     + hour + ':' + minute, '%d/%m/%Y %H:%M')
        except:
            tmp["data"] = datetime.datetime.strptime(str(day) + '/' + str(month) + '/' + str(year) + ' '
                                                     + "09" + ':' + "00", '%d/%m/%Y %H:%M')

        dateExam.append(tmp)

        exams = Exam.objects.all()

        cont = 0

        for ex in exams:
            if e == ex.nome and get_corso_di_studio_name(cod) == ex.facoltà.nome:
                cont += 1
                break
        if cont == 1:
            continue

        if e not in exam and e not in examNull:
            exam.append(e)
        else:
            continue


        driver.get("https://www.esse3.unimore.it/Guide/PaginaRicercaInse.do")
        select = Select(driver.find_element(By.XPATH, "//select[@id='facoltaPoli']"))
        select.select_by_value("F10005")
        select = Select(driver.find_element(By.XPATH, "//select[@id='annoAccademico']"))

        select.select_by_value(str(yea))
        select = driver.find_element(By.TAG_NAME, "input")
        select.clear()
        select.send_keys(createCourseString(cod))

        if check_exists_by_xpath(driver=driver, xpath="//button[@id='c-p-bn']"):
            driver.find_element(By.ID, "c-p-bn").click()

        try:
            driver.find_element(By.NAME, "actionBar1").click()
        except:
            print("Non esiste la facoltà scelta")
            setZero()
            return 0
        list = driver.find_element(By.ID, "risultati")

        if check_exists_by_xpath(list,"//*[contains(text(),'" + e + "')]"):
            list.find_element(By.XPATH, "//*[contains(text(),'" + e + "')]").click()
        else:
            exam.pop()
            examNull.append(e)
            continue
        table = driver.find_element(By.ID, "table1")
        table.find_element(By.XPATH, "//*[contains(text(),'" + cod + "')]").click()

        list = driver.find_elements(By.XPATH, "//div[@id='infobox']/dl")

        infoexam = []
        for el in list[0].text.split('\n'):
            infoexam.append(el)


        if "1°" in infoexam[1]:
            print(e + " è un esame del primo Anno")
            anno.append(1)
        elif "2°" in infoexam[1]:
            print(e + " è un esame del secondo Anno")
            anno.append(2)
        else:
            print(e + " è un esame del terzo Anno")
            anno.append(3)

        crediti.append(int(str(infoexam[5])))
        print(infoexam[5])

        if "Primo" in infoexam[13]:
            print("Primo Ciclo Semestrale")
            semestre.append(1)
        elif "Secondo" in infoexam[13]:
            print("Secondo Ciclo Semestrale")
            semestre.append(2)
        else:
            semestre.append(3)
        print("\n\n")

    tmp = [x for x in dateExam if x["exam"] not in examNull]
    setDateExam(tmp)
    print(dateExam)
    return 1


def setDateExam(date):
    global dateExam
    dateExam = date

def getValue(cod):
    global options
    for i in range(1, len(options)):
        if cod in options[i].text:
            return options[i]['value']
    return None


def print_dipartimento():
    url = 'https://www.esse3.unimore.it/Guide/PaginaListaAppelli.do'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    form = soup.find(id="FAC_ID")
    options = form.find_all("option")
    for i in range(1, len(options)):
        print(options[i].text)


def get_corso_di_studio_ingegneria():
    url = 'https://www.esse3.unimore.it/Guide/PaginaListaAppelli.do?FAC_ID=10005&CDS_ID=X&AD_ID=X&DOCENTE_ID=X&DATA_ESA=&actionBar1=1'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    form = soup.find(id="CDS_ID")
    global options
    options = form.find_all("option")

    for i in range(1, len(options)):
        triennOrmagi = options[i].text[4:7]
        if int(triennOrmagi) >= 250:
            durata.append(2)
        else:
            durata.append(3)

    return options

def get_corso_di_studio_name(cod):
    cds="-"
    for i in range(1, len(options)):
        if cod in options[i].text:
            cds = options[i].text
    return cds



def connectToAule(day, month, year):
    url = 'http://www.aule.unimore.it/index.php?page=3&content=view_prenotazioni&vista=day&area=27&_lang=it&day=' + day + '&month=' + month + '&year=' + year
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    exam_table = soup.find_all(attrs={"bgcolor": "#FFFFFF"})
    FAF = []
    FAg = []
    FAe = []
    aule = {}
    for e in exam_table:
        if "07:" in e.get('title', 'No title attribute') or "19:15" in e.get('title', 'No title attribute') or "20:" in e.get('title', 'No title attribute') or "21:" in e.get('title', 'No title attribute') or "22:" in e.get('title', 'No title attribute') or "23:" in e.get('title', 'No title attribute') or "19:30" in e.get('title', 'No title attribute'):
           pass
        else:
            if "FA-2F" in e.get('title', 'No title attribute'):
                FAF.append(e.get('title', 'No title attribute')[0:11])
            if "Fa-2g" in e.get('title', 'No title attribute'):
                FAg.append(e.get('title', 'No title attribute')[0:11])
            if "FA-2E" in e.get('title', 'No title attribute'):
                FAe.append(e.get('title', 'No title attribute')[0:11])

    aule['FA-2F'] = FAF
    aule['Fa-2g'] = FAg
    aule['FA-2E'] = FAe

    ret = {}
    ret['FA-2F'] = creaSpan(aule, 'FA-2F')
    ret['Fa-2g'] = creaSpan(aule, 'Fa-2g')
    ret['FA-2E'] = creaSpan(aule, 'FA-2E')

    return ret

def creaSpan(aule, aula):
    span = []
    for i in range(len(aule[aula])):
        if i == 0:
            print(aule[aula][i][:5])
            start = aule[aula][i][:5]
        else:
            if i == len(aule[aula])-1:
                print(aule[aula][i][6:])
                end = aule[aula][i][6:]
                span.append(start+'-'+end)
            elif aule[aula][i-1][6:] == aule[aula][i][:5]:
                continue
            else:
                print(aule[aula][i-1][6:])
                end = aule[aula][i-1][6:]
                span.append(start+'-'+end)
                print(aule[aula][i][:5])
                start = aule[aula][i][:5]
    return span


