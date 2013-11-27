from google.appengine.api import users
from datetime import date
import cgi
import urllib
import webapp2
import sys
import jinja2
import os
import cronjob
from lunardate import LunarDate
from messagingjob import MessagingJob
from google.appengine.api import users
from google.appengine.ext import ndb


DEFAULT_MESSAGING_JOB_NAME = 'default_job_queue'

## prevent flooding
MAX_ENTRIES_PER_USER=20

## Mostly set to prevent hitting Google AppEngine Email limits
MAX_ENTRIES_PER_DAY=8

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

def messagingJob_key(messaging_name=DEFAULT_MESSAGING_JOB_NAME):
    return ndb.Key('LunarCalendarReminderMessagingQueue', messaging_name)

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            pass
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            
            template_values = {
                    'jobs': '',
                    'logout_url': url,
                    'logout_url_linktext': url_linktext,
                    'error': self.request.get('msg',''),
                    }

            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))
            #self.redirect(users.create_login_url(self.request.uri))
            return

        messaging_jobs_query = MessagingJob.query(
            ancestor=messagingJob_key(DEFAULT_MESSAGING_JOB_NAME))
        messaging_jobs_query = messaging_jobs_query.filter(
            MessagingJob.owner == user).order(-MessagingJob.created_date)
        messaging_jobs = messaging_jobs_query.fetch(MAX_ENTRIES_PER_USER)

        logout_url = users.create_logout_url(self.request.uri)
        logout_url_linktext = 'Logout'

        template_values = {
                'jobs': messaging_jobs,
                'logout_url': logout_url,
                'logout_url_linktext': logout_url_linktext,
                'error': self.request.get('msg',''),
                }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class DeleteJob(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            pass
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
        msgJobKey=ndb.Key(urlsafe=self.request.get('id'))
        msgJobKey.delete()
        self.redirect('/?msg=success_deleted')




class AddJob(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            pass
        else:
            self.redirect(users.create_login_url(self.request.uri))


        msg_job_queue_name= DEFAULT_MESSAGING_JOB_NAME
        msg_job = MessagingJob(parent=messagingJob_key(msg_job_queue_name))

        msg_job.owner = users.get_current_user()

        msg_job.note = self.request.get('content')

        if self.request.get('date_type') == 'lunar':
            try:
                msg_job.date = LunarDate(int(self.request.get('year')),
                        int(self.request.get('month')), int(self.request.get('day'))).toSolarDate()
            except ValueError:
                self.redirect('/?msg=invalid_date')
                return
        else:
            try:
                msg_job.date = date(int(self.request.get('year')),
                        int(self.request.get('month')), int(self.request.get('day')))
            except ValueError:
                self.redirect('/?msg=invalid_date')
                return

        lunarDate=LunarDate.fromSolarDate(msg_job.date.year,msg_job.date.month,msg_job.date.day)
        msg_job.lunar_month = lunarDate.month
        msg_job.lunar_day = lunarDate.day

        base_messaging_jobs_query = MessagingJob.query(
            ancestor=messagingJob_key(DEFAULT_MESSAGING_JOB_NAME))
        messaging_jobs_query_by_user = base_messaging_jobs_query.filter(
            MessagingJob.owner == user)
        if messaging_jobs_query_by_user.count() >= MAX_ENTRIES_PER_USER:
            self.redirect('/?msg=exceed_user_quota')
            return

        messaging_jobs_query_by_date = base_messaging_jobs_query.filter(
                MessagingJob.lunar_month == msg_job.lunar_month).filter(
                MessagingJob.lunar_day == msg_job.lunar_day)
        if messaging_jobs_query_by_date.count() >= MAX_ENTRIES_PER_DAY:
            self.redirect('/?msg=exceed_daily_quota')
            return

        msg_job.put()

        self.redirect('/')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addJob', AddJob),
    ('/delete', DeleteJob),
    ('/cronjob/daily', cronjob.DailyEmail),
], debug=True)
