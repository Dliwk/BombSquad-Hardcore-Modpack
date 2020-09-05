from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Sequence, Optional

import time


def days_in_months(year: int) -> Sequence[Dict[int, int], int]:
    dm = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    if year % 4 == 0:
        dm[2] += 1
        return dm, 366
    return dm, 365


class Date(object):
    def __init__(self,
                 year: Optional[int] = None,
                 month: Optional[int] = None,
                 day: Optional[int] = None):
        self._is_formatted = False
        if year is None or month is None or day is None:
            now = self.now
            if year is None:
                year = now.year
            if month is None:
                month = now.month
            if day is None:
                day = now.day
            del now
        elif (year > 3000 or year < 1) or \
                (month < 1) or \
                (day > 30000 or day < 1):
            raise ValueError()
        self._year = year
        self._month = month
        self._day = day
        self.format_date()
        self._date = f'{self.year}.{self.month}.{self.day}'
        self._is_formatted = True

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month

    @property
    def day(self) -> int:
        return self._day

    @property
    def date(self) -> str:
        return self._date

    def format_date(self) -> None:
        dm, days = days_in_months(self._year)
        while True:
            while self._month > 12:
                for m in range(self._month - 12):
                    self._day += dm[(self._month % 12) + m]
                self._month -= 12
            while self._day > days:
                self._year += 1
                dm, days = days_in_months(self._year)
                self._day -= days
            while self._day > dm[(self._month % 12) + 1]:
                self._day -= dm[(self._month % 12) + 1]
                self._month += 1
            if (self._day < dm[self._month] and
                    self._month < 13):
                break

    @property
    def now(self) -> Date:
        now = time.strptime(time.ctime())
        return Date(year=now.tm_year,
                    month=now.tm_mon,
                    day=now.tm_mday)

    def __str__(self) -> str:
        return self._date

    def __bool__(self) -> bool:
        return bool(self.date <= self.now.date)

    def __setattr__(self, name, value) -> None:
        if getattr(self, '_is_formatted', False):
            raise Exception()
        return object.__setattr__(self, name, value)
