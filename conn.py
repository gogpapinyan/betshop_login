from ftplib import FTP
import json
from os import remove


class Ftp():

    def __init__(self, host, username, password):
        self.ftp = FTP(host)
        self.ftp.login(user=username, passwd=password)
        self.ftp.retrlines('LIST')

    def grabFile(self, fileName):
        localFile = open(fileName, 'wb')
        self.ftp.retrbinary('RETR ' + fileName, localFile.write)
        localFile.close()
        localString = open(fileName, 'r').read()
        dictionary = json.loads(localString)
        remove(fileName)
        return dictionary

    def quitFtp(self):
        self.ftp.quit()
