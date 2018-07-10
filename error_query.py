import cx_Oracle
import subprocess
import sys
import os
import time
import datetime
import signal

class SigTerm(SystemExit): pass
def sigterm(sig,frm): raise SigTerm
signal.signal(15,sigterm)

try:
    database = CONNECTION STRING
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
                f = open('error_log.txt', 'w')
                f.write(message)
                f.close()
                cmd1 = "ssh cgodfrey@cms904usr" 
                cmd2 = "python /nfshome0/cgodfrey/log4jDB/Log-Collector-DB/send_message.py"
                process = subprocess.Popen( "/bin/bash", shell=False, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
                out, err = process.communicate(cmd1 + "\n" + cmd2 + "\n")
        except Exception as e:
            print e
        time.sleep(60)

except BaseException as e:
    print e

finally:
    cur.close()
    connection.close()
