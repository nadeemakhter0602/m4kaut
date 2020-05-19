#IMPORT REQUIRED MODULES
#======================================================================================================#
import time
import os
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#VARIABLES
#======================================================================================================#
i=1
#SESSION REQUEST
#======================================================================================================#
while True:
    try:
        s=requests.session()
        rc=s.get('https://makaut1.ucanapply.com/smartexam/public/result-details',timeout=5)
    except Exception as f:
        os.system('clear')
        print(str(i)+'. '+str(f))
        i=i+1
        time.sleep(5)
        continue
    break
#COOKIE INITIALISATION
#=====================================================================================================#
cookies=rc.cookies.get_dict()
#POST REQUEST DATA
#=====================================================================================================#
data = {
  'p1': '',
  'ROLLNO': '',# Roll Number
  'SEMCODE': '',# Enter Semester in the format SM0X where X is the Semester
  'examtype': 'result-details',
  'all': ''
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://makaut1.ucanapply.com/smartexam/public/result-details',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',

    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}
#GET X-CSRF-TOKEN
#=====================================================================================================#
soup = BeautifulSoup(rc.content,features="html.parser")
token=soup.find("meta",{"name":"csrf-token"})['content']
data.update({'_token':token})
headers.update({'X-CSRF-TOKEN':token})
#CHECK AND GET RESULT
#=====================================================================================================#
while True:
    try:
        response=s.post('https://makaut1.ucanapply.com/smartexam/public/get-result-details',headers=headers,cookies=cookies,data=data,timeout=5)
    except Exception as e:
        os.system('clear')
        print(str(i)+". Error : "+str(e))
        i=i+1
        time.sleep(5)
        continue
    if 'Result under process!' in str(response.content):
        os.system('clear')
        print(str(i)+'. Result under Process')
        print(str(response.content))
        i=i+1
    elif '<Enter Name Here>' in str(response.content):
        os.system('clear')
        print(str(i)+". Result Released!")
        print(response.content)
        while True:
            try:
                response1=s.post('https://makaut1.ucanapply.com/smartexam/public/download-pdf-result',headers=headers,cookies=cookies,data=data,timeout=5)
            except Exception as e:
                os.system('clear')
                print(str(i)+". Error : "+str(e))
                i=i+1
                time.sleep(5)
                continue
            break
        with open("marksheet_<Roll Number here>.pdf","wb") as f:
            f.write(response1.content)
        for j in range('Start Roll Number','End Roll Number'):# For downloading multiple results, enter the start and end roll numbers in int format
            try:
                response2=s.post('https://makaut1.ucanapply.com/smartexam/public/download-pdf-result',headers=headers,cookies=cookies,data=data,timeout=5)
            except Exception as e:
                j=j-1
                print(str(i)+". Error : "+str(e))
                i=i+1
                time.sleep(5)
                continue
            with open("marksheet_"+str(j)+".pdf","wb") as f:
                f.write(response2.content)
        break
    time.sleep(60)
#SEND RESULT THROUGH EMAIL
#===========================================================================================================#
fromaddr = "<Enter Email>"
toaddr = "<Enter Email>"
   
# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# storing the senders email address   
msg['From'] = fromaddr 
  
# storing the receivers email address  
msg['To'] = toaddr 
  
# storing the subject  
msg['Subject'] = "<Enter Subject of Email>"
  
# string to store the body of the mail 
body = ""
  
# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
filename = "<Enter Desired Filename>"
attachment = open(filename, "rb") 
  
# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
p.set_payload((attachment).read()) 
  
# encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
msg.attach(p) 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login(fromaddr, "<Enter Email Password>") 
  
# Converts the Multipart msg into a string 
text = msg.as_string() 
  
# sending the mail 
s.sendmail(fromaddr, toaddr, text) 
  
# terminating the session 
s.quit() 
#================================================================================================#
        
# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form 
p.set_payload((attachment).read())

# encode into base64 
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg' 
msg.attach(p)

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security 
s.starttls()

# Authentication 
s.login(fromaddr, "<Enter Email Password>")

# Converts the Multipart msg into a string 
text = msg.as_string()

# sending the mail 
s.sendmail(fromaddr, toaddr, text)

# terminating the session 
s.quit()
#================================================================================================#

