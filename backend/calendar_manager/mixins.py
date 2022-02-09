import datetime


class MassCalandarGenerator(object):
    def _month_range(self, date, count):
        return [(date + datetime.timedelta(x * 365 / 12)).month for x in range(0, count)]

    def _which_weekday_in_month(self, day, month, year, current_datetime):
        dt = datetime.date(year, month, 1)
        dow_lst = []
        while dt.weekday() != day:
            dt = dt + datetime.timedelta(days=1)
        while dt.month == month:
            dow_lst.append(dt)
            dt = dt + datetime.timedelta(days=7)
        for index, item in enumerate(dow_lst):
            if item.day == current_datetime.day:
                return index

    def _dow_date_finder(self, which_weekday_in_month, day, month, year):
        dt = datetime.datetime(year, month, 1)
        dow_lst = []
        while dt.weekday() != day:
            dt = dt + datetime.timedelta(days=1)
        while dt.month == month:
            dow_lst.append(dt)
            dt = dt + datetime.timedelta(days=7)
        return dow_lst[which_weekday_in_month]

    def every_2end_date_month(self, date, count, **kwargs):
        index_week = self._which_weekday_in_month(date.weekday(), date.month, date.year, date)
        return [self._dow_date_finder(index_week, date.weekday(), month, date.year) for month in
                self._month_range(date, count)]

    def every_date_month(self, date, count, **kwargs):
        return [date.replace(month=x) for x in self._month_range(date, count)]

    def every_day_of_week(self, date, count, **kwargs):
        return [date + datetime.timedelta(days=x * 7) for x in range(0, count)]

    def every_day_of_week2(self, date, count, **kwargs):
        return [date + datetime.timedelta(days=x * 7) for x in range(0, count * 2)][::2]

    def every_day_of_week3(self, date, count, **kwargs):
        return [date + datetime.timedelta(days=x * 7) for x in range(0, count * 3)][::3]

    def every_day_of_week4(self, date, count, **kwargs):
        return [date + datetime.timedelta(days=x * 7) for x in range(0, count * 4)][::4]
