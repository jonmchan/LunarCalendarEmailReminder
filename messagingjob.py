from google.appengine.ext import ndb

class MessagingJob(ndb.Model):
    owner = ndb.UserProperty()
    date = ndb.DateProperty()
    note = ndb.StringProperty(indexed=False)
    created_date = ndb.DateProperty(auto_now_add=True)


