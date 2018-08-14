# Log-Collector-DB
This code reads logs from a DB for log collector interface to slack and web. It is a notification and monitioring system for HCAL online software logs. It consists of two components, a bot to send slack notifications in case of error and a web interface to search through the logs.

To run this program clone this repository to hcalmon and Web_Handsaw_Bot.py to cmshcalweb01. Slack webhooks and database connection strings that were removed when pushed to github must be added back locally.

The file structure should be as follows:
```
hcalmon:
    /var/www
        /cgi-bin/<LogCollectorDBDirName>
            web_queries.py
        /html/<RuninfoDifferDirName>
            index.html

cmshcalweb01:
    <nfshome0Dir>
        Web_Handsaw_Bot.py
```

To run the bot use the command:

```
sudo -u daqowner sh -c 'nohup python -u Web_Handsaw_Bot.py > WebHandsawLog.txt &'
```

Logging Collector Configuration:

To configure the logging collector edit the file on cmsrc-hcal: 
```
/opt/rcms/hcalpro/logcollector/tomcat/webapps/Collector/FileConfiguration/CollectorConfiguration.xml
```

the DBAppender section should look like the following (without comments):

```
<OUTPUT> <!-- DB -->
    <DBOutputName>DB</DBOutputName>                                               #Tell collector which appender it configuring           
    <DBOutputStatus>ON</DBOutputStatus>                                           #Turn on DBAppender
    <DBOutputLogLevel>INFO</DBOutputLogLevel>                                     #Write all messages of level INFO or above
    <DBOutputWorkingMode>QUEUE_WITH_NO_LOST_MSG</DBOutputWorkingMode>             #Create overflow queue and slow down message commit rate if it fills
    <DBOutputQueueMaxSize>1000</DBOutputQueueMaxSize>                             #Overflow queue size
    <DBOutputUrl>Connection String</DBOutputUrl>                                  #Database connection string
    <DBOutputUser>hcal_logcollector_admin</DBOutputUser>                          #Database account name
    <DBOutputPassword>DBPassword</DBOutputPassword>                               #Database password
    <DBOutputDriverClass>oracle.jdbc.driver.OracleDriver</DBOutputDriverClass>    #JDBC Driver used
    <DBOutputMessageCommitRate>10</DBOutputMessageCommitRate>                     #Messages commited at one time
    <DBOutputTimeoutCommitRate>5</DBOutputTimeoutCommitRate>                      #Commit Frequency
  </OUTPUT>
```

If a change to the configuration is made the tomcat must be restarted for it to take effect.
