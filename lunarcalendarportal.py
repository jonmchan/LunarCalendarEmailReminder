from google.appengine.api import users
from datetime import date
import cgi
import urllib
import webapp2
import sys
import jinja2
import os
from lunardate import LunarDate
from messagingjob import MessagingJob
from google.appengine.api import users
from google.appengine.ext import ndb

MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign" method="post">
      <div><label for="content">Reminder: </label><input name="content"
      type="text" /></div>
      <div>
      <label for="year">Year: </label>
      <select name="year">
      <option value="1900">1900</option>
      <option value="1901">1901</option>
      </select>
      
      <label for="month">Month: </label>
      <select name="month">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
      <option value="5">5</option>
      <option value="6">6</option>
      <option value="7">7</option>
      <option value="8">8</option>
      <option value="9">9</option>
      <option value="10">10</option>
      <option value="11">11</option>
      <option value="12">12</option>
      <option value="13">13 (lunar leap month)</option>
      </select>

      <label for="day">Day: </label>
      <select name="day">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
      <option value="5">5</option>
      <option value="6">6</option>
      <option value="7">7</option>
      <option value="8">8</option>
      <option value="9">9</option>
      <option value="10">10</option>
      <option value="11">11</option>
      <option value="12">12</option>
      <option value="13">13</option>
      <option value="14">14</option>
      <option value="15">15</option>
      <option value="16">16</option>
      <option value="17">17</option>
      <option value="18">18</option>
      <option value="19">19</option>
      <option value="20">20</option>
      <option value="21">21</option>
      <option value="22">22</option>
      <option value="23">23</option>
      <option value="24">24</option>
      <option value="25">25</option>
      <option value="26">26</option>
      <option value="27">27</option>
      <option value="28">28</option>
      <option value="29">29</option>
      <option value="30">30</option>
      <option value="31">31</option>
      </select>
      </div>
      <div><input type="submit" value="Add Email Reminder"></div>
    </form>

    <hr>

    <a href="%s">%s</a>

  </body>
</html>
"""



DEFAULT_MESSAGING_JOB_NAME = 'default_job_queue'

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
            self.redirect(users.create_login_url(self.request.uri))

        #self.response.write('<html><body>')

        messaging_jobs_query = MessagingJob.query(
            ancestor=messagingJob_key(DEFAULT_MESSAGING_JOB_NAME))
        messaging_jobs_query = messaging_jobs_query.filter(
            MessagingJob.owner == user).order(-MessagingJob.created_date)
        messaging_jobs = messaging_jobs_query.fetch(10)

        #for job in messaging_jobs:
        #    self.response.write(
        #            '<b>%s</b> wrote: <a href="/delete?id=%s">Delete</a>' %
        #            (job.date,job.key.urlsafe()))
        #    self.response.write('<blockquote>%s</blockquote>' %
        #                        cgi.escape(job.note))
            
        logout_url = users.create_logout_url(self.request.uri)
        logout_url_linktext = 'Logout'

        # Write the submission form and the footer of the page
        #sign_query_params = urllib.urlencode({'guestbook_name': DEFAULT_MESSAGING_JOB_NAME })
        #self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
        #                    (sign_query_params, url, url_linktext))

        template_values = {
                'jobs': messaging_jobs,
                'logout_url': logout_url,
                'logout_url_linktext': logout_url_linktext,
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
        self.redirect('/')




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

        msg_job.date = date(int(self.request.get('year')),
                int(self.request.get('month')), int(self.request.get('day')))
        msg_job.put()

        self.redirect('/')
        

        #self.response.write('<html><body>'+user.email()+' wrote:<pre>')
        #self.response.write(cgi.escape(self.request.get('content')))
        #self.response.write('</pre></body></html>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addJob', AddJob),
    ('/delete', DeleteJob),
], debug=True)
