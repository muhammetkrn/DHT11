import grovepi
import time
import smtplib
import time
import requests
dht_sensor_port=4
dht_sensor_type=0
data=open('data.txt','w')
[ temp,hum ] = grovepi.dht(dht_sensor_port,dht_sensor_type)
ip_request = requests.get('https://get.geojs.io/v1/ip.json')
my_ip = ip_request.json()['ip']
#print(my_ip)
geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
geo_request = requests.get(geo_request_url)
geo_data = geo_request.json()
org=geo_data["organization"]
neworg=org.replace(" ","_")
print ('Temp: '+ str(temp) + '*C' + '\tHumidity:' + ' %'+ str(hum) + ' ' + str(time.strftime("%s",time.gmtime())))
data.write('temperature,location=' + neworg + ' temp='+ str(temp))
data.write('\n')
data.write('temperature,location=' + neworg +  ' hum='+ str(hum))

def mail(content):
    mail = smtplib.SMTP("smtp.gmail.com",587) 
    mail.starttls()
    mail.login('gozenintern@gmail.com','iskenHub123**')
    mail.sendmail("gozenintern@gmail.com","muhammetkrn19@gmail.com",content)


if temp>=25.0:
    content = 'Oda sicakligi ' + str(temp) + '*C' + ' Sicaklik yuksek!'
    mail(content)
elif temp<=15:
    content = 'Oda sicakligi ' + str(temp) + '*C' + ' Sicakligi artirmaniz onerilir.'
    mail(content)
elif hum >=35:
    content = 'Odadaki nem orani  %' +  str(hum)  + ' Nem orani cok yuksek!'
    mail(content)
elif hum <=15:
    content = 'Odadaki nem orani  %' +  str(hum)  + ' Nem orani cok dusuk!'
    mail(content)
