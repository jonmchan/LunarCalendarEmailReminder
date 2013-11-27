import logging
from google.appengine.ext import ndb
import datetime
from lunardate import LunarDate
from messagingjob import MessagingJob

BATCH_SIZE=100

def UpdateSchema(cursor=None,num_updated=0):
    query = MessagingJob.query()

    results, cursor, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)

    to_put = []
    for p in results:
        # migration #1 - AppVersion 2 - adding lunar_month & lunar_day index
        if p.lunar_month is None and p.lunar_day is None:
            lunarDate=p.getLunarDate()
            p.lunar_month=lunarDate.month
            p.lunar_day=lunarDate.day
            logging.info(str(p.getLunarDate()) + p.note + " migrated")
        else:
            logging.info(str(p.getLunarDate()) + p.note + " does not have an empty lunar_month/lunar_date")
            continue

        to_put.append(p)

    if to_put:
        ndb.put_multi(to_put)
        num_updated += len(to_put)
        logging.debug('Put %d entities to Datastore for a total of %d',
                len(to_put),num_updated)
        if more:
            deferred.defer(
                    UpdateSchema, cursor, num_updated)
        else:
            logging.info("Updated schema <MessagingJob> with %d updates" % (
                num_updated))

    return


