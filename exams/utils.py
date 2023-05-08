from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import DateExam
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, id=0, checklist=[]):
        self.year = year
        self.month = month
        self.id = id
        self.checklist = checklist
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(data__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event.exam}<br>{event.data.time()} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
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
        events = events.order_by("data")
        cal = f'<table style="width:70%" border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'</table>'
        return cal
