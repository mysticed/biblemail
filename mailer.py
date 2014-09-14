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
        options = ['reading-plan=bcp']
        url = self.baseUrl + 'readingPlanInfo?key=%s&date=%s&%s' % (self.key, readingDate.isoformat(), '&'.join(options))
        page = urllib.urlopen(url)
        tree = ET.fromstring(page.read())      
        return self.getPassage(tree.find('info').find('gospel').text)
   
bible = BibleSession('IP')
    
fromaddr = 'mysticed@gmail.com'
toaddrs  = 'mysticed@gmail.com'
subject = 'Subject'

message = MIMEMultipart('alternative')
message['Subject'] = subject
message['From'] = fromaddr
message['To'] = toaddrs

htmlPart = MIMEText(bible.getGospelReading(datetime.date.today()), 'html')
message.attach(htmlPart)

username = 'mysticed@gmail.com'
password = 'fvrxuvmowufixaci'

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, message.as_string())
server.close()

