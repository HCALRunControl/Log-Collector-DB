#!/usr/bin/python
import cx_Oracle
import subprocess
import sys
import os
import time
import datetime
import signal
import cgi
import cgitb; cgitb.enable()
from commands import getoutput
 



class SigTerm(SystemExit): pass
def sigterm(sig,frm): raise SigTerm
signal.signal(15,sigterm)

def is_timestamp(data):
    try:
        datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
        return True
    except ValueError:
        return False

def is_an_int(data):
    try:
        int(data)
        return True
    except ValueError:
        return False

def build_query(num_messages, level, timestamp, app_name, port): 

    levels = ("DEBUG", "INFO", "WARN", "ERROR", "FATAL")
    required_level = str(levels[levels.index(level):])
    filter1 =  "SELECT * FROM LOG_EVENT WHERE TIMESTAMP < TO_TIMESTAMP(\'" + str(timestamp) + "', 'YYYY-MM-DD HH24:MI:SS.FF')"
    filter2 = 'SELECT * FROM (' + filter1 + ') WHERE LEVEL_STRING IN ' + required_level + 'AND UPPER(LOGGER_NAME) LIKE \'%' + app_name.upper() + '%\'AND LOGGER_NAME LIKE \'%' + str(port) + '%\' ORDER BY TIMESTAMP DESC'
    filter3 = 'SELECT * FROM (' + filter2 + ') WHERE ROWNUM <= ' + str(num_messages)            

    return filter3

def execute_query():
    try:
        database = 'CONNECTION_STRING'
        connection = cx_Oracle.connect(database)
        global cur
        cur = connection.cursor()
        SQL = build_query(numberOfLines, filterLevel, time, name, port) 
        #SQL = build_query(4, "WARN", datetime.datetime.now(), "", "")
        cur.execute(SQL)
        query_result = cur.fetchall()
        return query_result

    except Exception as e:
        print e


    finally:
        cur.close()
        connection.close()
        #print "safe"


def getHeader():
    header = """
            <html>
                <head>
                    <title>Log Viewer</title> 
                </head>
                <body>
            """
    return header



def getFooter():
  footer =  """
            <!-- begin footer -->
            </body>
        </html>
       """
  return footer


form = cgi.FieldStorage()
numberOfLines =  form.getvalue('numberOfLines', 10)
filterLevel =  form.getvalue('filter', 'ERROR')
time = form.getvalue('timestamp', datetime.datetime.now())
name = form.getvalue('appName', "")
port = form.getvalue('port', 0)

colormap = {'INFO':'#00ae00', 'WARN':'#e8e866', 'ERROR':'#DF0000'}

print "Content-type: text/html"
print getHeader()
if (is_an_int(numberOfLines) and is_an_int(port)):
    log = execute_query()
    for line in reversed(log):
        fields = {'timestamp':line[1], 'message':line[2], 'logger':line[3], 'level':line[4]}
        time = str(fields['timestamp']).split('.')[0]
        milliseconds = str(fields['timestamp']).split('.')[1][:3]
        print "<span style=\"background-color:" + colormap[fields['level']] + "\">" + time + ' and ' + milliseconds + '  ms' + " : " + fields['logger'] + " " + fields['level'] + "</span>" + "<br>" + "<span style=\"text-indent:2em\">" + fields['message'] + "</span>" + "<br>"
else:
    print "input correct datatypes"

print getFooter()



