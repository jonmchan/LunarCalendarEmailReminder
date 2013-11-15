from lunardate import LunarDate
from messagingjob import MessagingJob
import webapp2
import datetime
import lunarcalendarportal
from google.appengine.api import mail

SENDER="Lunar Calendar Reminder <lunar-calendar-email-reminder@appspot.gserviceaccount.com>"

EMAIL_BODY="""Dear %s,

We are writing you to remind you of the following event that you set on the
lunar calendar reminder:

    %s

Your next reminder will be sent: %s

You may enable/disable this event by visiting the webpage. Thank you for using
this service!


Lunar Calendar Reminder
"""

class DailyEmail(webapp2.RequestHandler):
    def get(self):
        today_ld=LunarDate.today()
        q1=MessagingJob.query()
        for job in q1.iter():
            original_ld=LunarDate.fromSolarDate(job.date.year, job.date.month, job.date.day)
            if original_ld.month == today_ld.month and original_ld.day == today_ld.day:
                mail.send_mail(sender=SENDER,
                        to=job.owner.email(),
                        subject="Lunar Calendar Reminder - "+job.note,
                        body= EMAIL_BODY % (job.owner.nickname(),
                            job.note, job.getNextRun))
