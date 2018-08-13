import cx_Oracle
import subprocess
import sys
import os
import time
import datetime
import signal
import requests
import json
reload(sys)


class SigTerm(SystemExit): pass
def sigterm(sig,frm): raise SigTerm
signal.signal(15,sigterm)

def sendSlackMessage(alert):
    print alert
    webhook_url = "https://hooks.slack.com/services/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"
    slack_data = {'text': "Testing new webHandsaw System ```%s```" % alert}
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        print 'Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text)
        return False
    else:
        return True

try:
    database = "hcallog4jdb_admin/HCAL_4jlogger@int2r1-v.cern.ch:10121/int2r_lb.cern.ch"
    connection = cx_Oracle.connect(database)
    global cur
    cur = connection.cursor()
    last_query = datetime.datetime.now()
    while True:
        try:    
            SQL = "SELECT MESSAGE, TIMESTAMP FROM (SELECT * FROM LOG_EVENT WHERE LEVEL_STRING IN ('ERROR', 'FATAL') ORDER BY ID DESC) WHERE (TIMESTAMP > TO_TIMESTAMP('" + str(last_query) + "', 'YYYY-MM-DD HH24:MI:SS.FF'))"
            last_query = datetime.datetime.now()
            cur.execute(SQL)
            query_result = cur.fetchall()
            print query_result
            for error in query_result:
                print "check"
                message = error[0]
                timestamp = error[1]
            sendSlackMesssage(message)
        except Exception as e:
            print e
        time.sleep(60)

except BaseException as e:
    print e

finally:
    cur.close()
    connection.close()