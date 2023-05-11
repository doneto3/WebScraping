from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import DateExam, Aula
import time
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, id=0, checklist=[], checkspan=[], span=0):
        self.year = year
        self.month = month
        self.id = id
        self.checklist = checklist
        self.checkspan = checkspan
        self.span = span
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, weekday, events, aula):
        events_per_day = events.filter(data__day=day)
        aula = aula.filter(data__day=day)
        d = ''
        if not events_per_day and weekday != 5 and weekday != 6:
            for a in aula:
                d += f'<li id=\'room\'><b>{a.get_nome_display()}</b><br>{a.span_disponibilità}</li>'
        else:
            for event in events_per_day:
                d += f'<li id=\'event\' > {event.exam}<br>{event.data.time()} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, aula):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, weekday, events, aula)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        aula = Aula.objects.filter(data__year=self.year, data__month=self.month)
        events = DateExam.objects.filter(exam__facoltà_id=self.id, data__year=self.year, data__month=self.month)
        if not self.checklist:
            pass
        elif 1 not in self.checklist and 2 not in self.checklist and 3 not in self.checklist:
            if 4 not in self.checklist:
                events = events.exclude(exam__semestre=1)
            if 5 not in self.checklist:
                events = events.exclude(exam__semestre=2)
            if 6 not in self.checklist:
                events = events.exclude(exam__semestre=3)
        elif 4 not in self.checklist and 5 not in self.checklist and 6 not in self.checklist:
            if 1 not in self.checklist:
                events = events.exclude(exam__anno=1)
            if 2 not in self.checklist:
                events = events.exclude(exam__anno=2)
            if 3 not in self.checklist:
                events = events.exclude(exam__anno=3)
        else:
            if 1 not in self.checklist:
                events = events.exclude(exam__anno=1)
            if 2 not in self.checklist:
                events = events.exclude(exam__anno=2)
            if 3 not in self.checklist:
                events = events.exclude(exam__anno=3)
            if 4 not in self.checklist:
                events = events.exclude(exam__semestre=1)
            if 5 not in self.checklist:
                events = events.exclude(exam__semestre=2)
            if 6 not in self.checklist:
                events = events.exclude(exam__semestre=3)
        if 1 not in self.checkspan:
            aula = aula.exclude(nome=1)
        if 2 not in self.checkspan:
            aula = aula.exclude(nome=2)
        if 3 not in self.checkspan:
            aula = aula.exclude(nome=3)
        events = events.order_by("data")
        aula = aula.order_by("nome")
        if self.span != 0:
            for a in aula:
                start_time, end_time = a.span_disponibilità.split('-')
                start_time = datetime.strptime(start_time, '%H:%M')
                end_time = datetime.strptime(end_time, '%H:%M')

                duration = end_time - start_time

                if duration < timedelta(minutes=self.span):
                    aula = aula.exclude(data=a.data, nome=a.nome, span_disponibilità=a.span_disponibilità)
                else:
                    continue
        cal = f'<table style="width:70%" border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        start = time.time()
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, aula)}\n'
        end = time.time()
        print(end-start)
        cal += f'</table>'
        return cal
