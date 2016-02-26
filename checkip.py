import smtplib
import urllib
import re
import json
import time

class Registro(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = json.load(open(self.filename))
    
    def checkAddress(self):
        site = urllib.urlopen(self.file["urls"]["check_ip"])
        grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site.read())
        address = grab[0]
        old_ip = self.getLastIP()
        if old_ip != address:
            self.file["urls"]["last_ip"] = address
            self.file["urls"]["last_ip_updated"] = time.strftime("%c")
            json.dump(self.file, open(self.filename, "w"), sort_keys = False, indent = 4)
            return True
        else:
            return False
    
    def getLastIP(self):
        return self.file["urls"]["last_ip"]            


class Gmail(object):
    def __init__(self, filename):
        self.file = json.load(open(filename))
        self.email = self.file["Gmail"]["email"]
        self.emailto = self.file["Gmail"]["emailto"]
        self.password = self.file["Gmail"]["password"]
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)        
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message(self, subject, body):
        ''' This must be removed '''
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + self.emailto,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            self.email,
            headers + "\r\n\r\n" + body)


gm = Gmail('./checkip.json')
reg = Registro('./checkip.json')

if reg.checkAddress():
    gm.send_message('New IP', reg.getLastIP())