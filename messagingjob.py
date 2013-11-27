from google.appengine.ext import ndb
from lunardate import LunarDate
import datetime


class MessagingJob(ndb.Model):
    owner = ndb.UserProperty()
    date = ndb.DateProperty()
    note = ndb.StringProperty(indexed=False)
    created_date = ndb.DateProperty(auto_now_add=True)
    lunar_month = ndb.IntegerProperty(indexed=True)
    lunar_day = ndb.IntegerProperty(indexed=True)


    def getLunarDate(self):
        ld = LunarDate.fromSolarDate(self.date.year, self.date.month,self.date.day)
        return ld

    def getFormattedLunarDate(self):
        ld = self.getLunarDate()
        return str(ld.year) + "/"+ str(ld.month)+"/"+str(ld.day)

    def getNextRun(self):
        try:
            ld = self.getLunarDate()
            if datetime.date.today() < LunarDate(datetime.date.today().year,ld.month,ld.day).toSolarDate():
                ld = LunarDate(datetime.date.today().year,ld.month,ld.day)
            else:
                ld= LunarDate(datetime.date.today().year+1,ld.month,ld.day)
            return ld.toSolarDate().strftime('%m/%d/%Y')
        except ValueError:
            return "Date before 1900 or after 2050 Error"



