# Lunar Calendar Email Reminder

This application is a simple set and forget email reminder tool that will send an email out to remind you of an event in the lunar calendar. It is useful for getting reminders for Asian parents or grandparents that celebrate their birthday in the lunar calendar or to remind you of any other lunar calendar events. You can also use this to find out your lunar birthday by entering in your western birthday with the year.

I could not find this functionality in google calendar so I wrote this application very quickly to fill in this gap. This application will work until 2050 and then it will stop working because of a limitation in the lunar conversion library I am using. Hopefully I will update it before then!

## Installation

You simply deploy this project to AppEngine. Create your own project in
AppEngine and simply deploy to that project. Make sure to change the app.yaml
application name to your own custom name or the AppEngine deploy script will try
to deploy to the production instance.

## Upgrading

If you are upgrading from an old version of Lunar Calendar Email Reminder, some
of the entities may have changed and you may have to run the schema migration 
tool. You can do this by going to ```/update_schema``` url endpoint as an
administrator. If it is successful, you can expect to see a similar line as this
in the logs:

```
2013-11-27 10:36:36.619 /_ah/queue/deferred 200 185ms 0kb AppEngine-Google; (+http://code.google.com/appengine) module=default version=2
I 2013-11-27 10:36:36.438 X-Appengine-Taskretrycount:0, X-Appengine-Tasketa:1385566510.916393, X-Appengine-Taskname:1305632493100163229, X-Appengine-Taskexecutioncount:0, X-App
D 2013-11-27 10:36:36.618 Put 4 entities to Datastore for a total of 4
I 2013-11-27 10:36:36.618 Updated schema <MessagingJob> with 4 updates
```

You do not need to run this if this is the first time you are installing the system.


## Production Url:

[http://lunar-date-reminder.appspot.com/](http://lunar-date-reminder.appspot.com/)

## Known Issues:

* If you sign in with Multiple Sign On with google, you may get a 500 error. Use a Google Chrome incognito session or sign out of all your other email accounts as a workaround for now. If I find a solution, I'll fix it.
