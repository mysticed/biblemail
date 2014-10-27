import urllib
import sys
import os
import datetime
import xml.etree.ElementTree as ET
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class BibleSession:
    def __init__(self, key):
        self.baseUrl = 'http://www.esvapi.org/v2/rest/'
        self.key = key
        self.readings = [
            'Luke 1:1-4',
            'Luke 1:5-25',
            'Luke 1:26-38',
            'Luke 1:39-56',
            'Luke 1:57-80',
            'Luke 2:1-20',
            'Luke 2:21-40',
            'Luke 2:41-52',
            'Luke 3:1-9',
            'Luke 3:10-20',
            'Luke 3:21-38',
            'Luke 4:1-13',
            'Luke 4:14-30',
            'Luke 4:31-44',
            'Luke 5:1-11',
            'Luke 5:12-16',
            'Luke 5:17-26',
            'Luke 5:27-39',
            'Luke 6:1-11',
            'Luke 6:12-26',
            'Luke 6:27-38',
            'Luke 6:39-49',
            'Luke 7:1-10',
            'Luke 7:11:17',
            'Luke 7:18-35',
            'Luke 7:36-50',
            'Luke 8:1-15',
            'Luke 8:16-25',
            'Luke 8:26-39',
            'Luke 8:40-56',
            'Luke 9:1-17',
            'Luke 9:18-27',
            'Luke 9:28-45',
            'Luke 9:46-62',
            'Luke 10:1-16',
            'Luke 10:17-24',
            'Luke 10:25-37',
            'Luke 10:38-42',
            'Luke 11:1-13',
            'Luke 11:14-28',
            'Luke 11:29-41',
            'Luke 11:42-54',
            'Luke 12:1-12',
            'Luke 12:13-34',
            'Luke 12:35-48',
            'Luke 12:49-59',
            'Luke 13:1-9',
            'Luke 13:10-21',
            'Luke 13:22-30',
            'Luke 13:31-35',
            'Luke 14:1-11',
            'Luke 14:12-24',
            'Luke 14:25-35',
            'Luke 15:1-10',
            'Luke 15:11-24',
            'Luke 15:25-32',
            'Luke 16:1-9',
            'Luke 16:10-18',
            'Luke 16:19-31',
            'Luke 17:1-10',
            'Luke 17:11-19',
            'Luke 17:20-37',
            'Luke 18:1-14',
            'Luke 18:15-30',
            'Luke 18:31-43',
            'Luke 19:1-10',
            'Luke 19:11-27',
            'Luke 19:28-40',
            'Luke 19:41-48',
            'Luke 20:1-8',
            'Luke 20:9-19',
            'Luke 20:20-26',
            'Luke 20:27-40',
            'Luke 20:41-21:4',
            'Luke 21:5-19',
            'Luke 21:20-33',
            'Luke 21:34-38',
            'Luke 22:1-23',
            'Luke 22:24-38',
            'Luke 22:39-53',
            'Luke 22:54-71',
            'Luke 23:1-12',
            'Luke 23:13-26',
            'Luke 23:27-43',
            'Luke 23:44-56',
            'Luke 24:1-12',
            'Luke 24:13-27',
            'Luke 24:28-35',
            'Luke 24:36-53'
            ]

    def getPassage(self, passage):
        passage = passage.split()
        passage = '+'.join(passage)
        options = ['include-short-copyright=true',
            'include-passage-horizontal-lines=0',
            'include-heading-horizontal-lines=0',
            'include-verse-numbers=false',
            'include-footnotes=false',
            'include-audio-link=true',
            'audio-format=mp3']
        url = self.baseUrl + 'passageQuery?key=%s&passage=%s&%s' % (self.key, passage, '&'.join(options))
        page = urllib.urlopen(url)
        return page.read()
    
    def getGospelReading(self, readingDate):      
        #options = ['reading-plan=bcp']
        #url = self.baseUrl + 'readingPlanInfo?key=%s&date=%s&%s' % (self.key, readingDate.isoformat(), '&'.join(options))
        #page = urllib.urlopen(url)
        #tree = ET.fromstring(page.read())      
        #return self.getPassage(tree.find('info').find('gospel').text)
        date0 = datetime.date(2014, 10, 23)
        delta = readingDate - date0
        return self.getPassage(self.readings[delta.days])
   
bible = BibleSession('IP')
    
fromaddr = 'ed@robinsonmail.me.uk'
toaddrs  = 'mysticed@gmail.com'
subject = 'Bible Reading ' + datetime.date.today().isoformat()

message = MIMEMultipart('alternative')
message['Subject'] = subject
message['From'] = fromaddr
message['To'] = toaddrs

htmlPart = MIMEText(bible.getGospelReading(datetime.date.today()), 'html')
message.attach(htmlPart)

username = os.environ.get('POSTMARK_API_KEY')
password = os.environ.get('POSTMARK_API_KEY')

server = smtplib.SMTP('smtp.postmarkapp.com', 587)
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, [toaddrs, fromaddr], message.as_string())
server.close()

