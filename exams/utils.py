from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import DateExam

global i, f
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(data__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def getI(self, ida, idf):
        global i, f
        i = ida
        f = idf
    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        global i, f
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

        events = DateExam.objects.filter(exam__facoltà_id=f,data__year=self.year, data__month=self.month, exam__anno=a, exam__semestre=s)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
