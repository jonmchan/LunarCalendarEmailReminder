import webapp2
import logging
import migrations

from google.appengine.ext import deferred

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("we made it here")
        deferred.defer(migrations.UpdateSchema)
        self.response.out.write('Schema migration successfully initiated.')


app = webapp2.WSGIApplication([('/update_schema',UpdateHandler)], debug=True)
