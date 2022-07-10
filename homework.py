from ctypes import Union
from datetime import date as dt
import datetime as dtime


class Record:
    def __init__(self, amount: float, comment: str,
                 date=None) -> None:
        if date is None:
            self.date = dt.today()
        else:
            date_list = [int(i) for i in date.split(".")]
            d = dtime.date(date_list[2], date_list[1], date_list[0])
            self.date = d
        self.amount = amount
        self.comment = comment


class Calculator:
    def __init__(self, limit: float) -> None:
        self.used = 0
        self.limit = limit
        self.records = list()

    def add_record(self, record: Record):
        self.records.append(record)
        self.used = record.amount + self.used

    def get_today_stats(self) -> float:
        spent_today = 0
        for i in self.records:
            if(i.date == dt.today()):
                spent_today = i.amount + spent_today
        self.spent_today = spent_today
        return spent_today

    def get_week_stats(self) -> float:
        count = 0
        today = dtime.date.today()
        date_week_ago = today - dtime.timedelta(days=7)
        for i in self.records:
            if i.date <= today and i.date >= date_week_ago:
                count = count + i.amount
        return count


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        spent_today = Calculator.get_today_stats(self)
        if self.limit > spent_today:
            return(f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.limit - spent_today} кКал')
        elif self.limit <= spent_today:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = 84.
    EURO_RATE = 95.
    RUB_RATE = 1.

    def get_today_cash_remained(self, currency="rub") -> str:
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        spent_today = Calculator.get_today_stats(self)
        cash_remained = self.limit - spent_today
        if cash_remained == 0:
            return 'Денег нет, держись'
        name, rate = currencies[currency]
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            message = f'На сегодня осталось {cash_remained} {name}'
        else:
            cash_remained = abs(cash_remained)
            message = (f'Денег нет, держись: твой долг - {cash_remained} '
                       f'{name}')
        return message
