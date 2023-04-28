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

dipartimento = {"303": "10013",
                "103": "10002",
                "150": "10003",
                "183": "10014",
                "111": "10004",
                "120": "10005",
                "304": "10015",
                "301": "10011",
                "116": "10006",
                "117": "10007",
                "101": "10008",
                "216": "10009",
                "302": "10012",
                "112": "10010",
                "114": "10053",
                "11": "7"}

corso_di_studio_ingegneria = {
    "20-269": "10668",
    "20-218": "10727",
    "20-268": "10582",
    "20-200": "229",
    "20-206": "235",
    "20-267": "10358",
    "20-210": "10294",
    "20-270": "10726",
    "20-203": "232",
    "20-266": "10304",
    "20-204": "233",
    "20-216": "10667",
    "20-264": "10302",
    "20-201": "230",
    "20-261": "10299",
    "20-215": "10359",
    "20-202": "231",
    "20-212": "10296",
    "20-262": "10300",
    "20-217": "10706",
    "20-205": "234",
    "20-213": "10297",
    "20-263": "10301",
    "20-265": "10303"
}

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

def connectToEsse3Page(cod):
    global anno, semestre, crediti, exam, durata, dateExam, examNull
    cds_id = corso_di_studio_ingegneria.get(cod)
    url = 'https://www.esse3.unimore.it/Guide/PaginaListaAppelli.do?FAC_ID=10005&CDS_ID=' + cds_id + '&AD_ID=X&DOCENTE_ID=X&DATA_ESA=&actionBar1=1'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver = ChromeDriverManager().install()
    driver = Chrome(service=Service(chrome_driver), options=chrome_options)
    exam_table = soup.find(attrs={"class": "table-1-body"})
    table_elem = exam_table.find_all("tr")
    setZero()

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
            hour = int(turno[13:15])
            minute = int(turno[16:18])
            # response = GoogleCalendar.create_event(calendar_id, summary, description, day, month, year, hour, minute)
            # print(response['summary'])
            time.sleep(0.005)
        except:
            hour = 9
            minute = 0
            # response = GoogleCalendar.create_event(calendar_id, summary, description, day, month, year, hour, minute)
            # print(response['summary'])
            time.sleep(0.005)

        print(summary + '\n' + description + '\n' + str(day) + '/' + str(month) + '/' + str(year) + ' ' + str(
            hour) + ':' + str(minute) + '\n')

        for e in summary.split('] '):
            continue
        print(i)
        if '\'' in e:
            e = apostrofoString(e)



        tmp["exam"] = e
        tmp["tipo"] = tipo
        tmp["docente"] = docente
        tmp["num_iscr"] = num_iscr
        tmp["data"] = datetime.datetime.strptime(str(day) + '/' + str(month) + '/' + str(year), '%d/%m/%Y')

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



        today = datetime.date.today()

        year = today.year
        year -= 1

        select.select_by_value(str(year))
        select = driver.find_element(By.TAG_NAME, "input")
        select.clear()
        select.send_keys(createCourseString(cod))

        if check_exists_by_xpath(driver=driver, xpath="//button[@id='c-p-bn']"):
            driver.find_element(By.ID, "c-p-bn").click()


        driver.find_element(By.NAME, "actionBar1").click()
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
        # exit(0)


def setDateExam(date):
    global dateExam
    dateExam = date

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

