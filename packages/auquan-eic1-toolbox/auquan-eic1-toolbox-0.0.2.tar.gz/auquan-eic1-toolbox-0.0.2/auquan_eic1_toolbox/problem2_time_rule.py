from backtester.timeRule.custom_time_rule import CustomTimeRule
from datetime import datetime, timedelta
import pandas as pd
from pandas.tseries.offsets import CustomBusinessHour
from pandas.tseries.offsets import CustomBusinessDay

#change name to problem1_time_rule.py

class DayTimeRule(CustomTimeRule):
    def __init__(self, startDate, endDate, startTime='9:00', endTime='16:00', holidays = [], weekmask = 'Mon Tue Wed Thu Fri', calendar = None, frequency='H', sample='1'):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__sample = sample

        acceptable_freq = ['D', 'M', 'H', 'S', 'Mo']
        if frequency not in acceptable_freq:
            raise ValueError('Frequency Value Not acceptable. Specify D, M, H, S')
        self.__frequency = frequency

        start = datetime.strptime(startTime, '%H:%M')
        self.startMinuteDelta = start.hour * 60 + start.minute
        end = datetime.strptime(endTime, '%H:%M')
        self.endMinuteDelta = end.hour * 60 + end.minute

        if(calendar != None):
            self.__bday = CustomBusinessDay(calendar = calendar)
            self.__bhour =  CustomBusinessHour(start = startTime, end = endTime, calendar = calendar)
        else:
            self.__bday = CustomBusinessDay(holidays = holidays, weekmask = weekmask)
            self.__bhour = CustomBusinessHour(start = startTime, end = endTime, holidays = holidays, weekmask = weekmask)

    def createBusinessMonthSeries(self):
        return pd.date_range(self.__startDate, self.__endDate , freq= self.__sample + 'M')

    def emitTimeToTrade(self):
        time_range = None
        if(self.__frequency == 'D'):
            time_range = self.createBusinessDaySeries()
        elif(self.__frequency == 'H'):
            time_range = self.createBusinessHourSeries()
        elif(self.__frequency == 'M'):
            time_range = self.createBusinessMinSeries()
        elif(self.__frequency == 'S'):
            time_range = self.createBusinessSecSeries()
        elif(self.__frequency == "Mo"):
            time_range = self.createBusinessMonthSeries()
        for timestamp in time_range:
            yield timestamp
