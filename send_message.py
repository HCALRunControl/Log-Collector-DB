import sys
import requests
import json
import subprocess
reload(sys)


def sendSlackMessage(alert):
    print alert
    webhook_url = WEBHOOK
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

f = open('/nfshome0/cgodfrey/log4jDB/Log-Collector-DB/error_log.txt', 'r')
message = f.read()
f.close()
sendSlackMessage(message)
    
