import grovepi
import time
import smtplib
import time
import requests
dht_sensor_port=4 #Sensörümüzün GrovePi cihazı üzerinde D4 portuna takılı.
dht_sensor_type=0 #Sıcaklık ve Nem ölçen sensörün DHT11 olduğunu gösterir. (Sensörümüz DHT22 olsaydı type'ı '1' olarak alacaktık.)
data=open('data.txt','w') #data.txt dosyası yazılmak için açılıyor.
[ temp,hum ] = grovepi.dht(dht_sensor_port,dht_sensor_type) #Cihazın algıladığı sıcaklık ve nem değerlerini, sırasıyla temp ve hum değişkenine atıyor.
ip_request = requests.get('https://get.geojs.io/v1/ip.json') #https://get.geojs.io sitesiyle bağlantı kuruluyor.
my_ip = ip_request.json()['ip'] #https://get.geojs.io sitesi üzerinden ip değeri çekiliyor.
#print(my_ip) #ip değerimiz ekrana yazdırılıyor.
geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
geo_request = requests.get(geo_request_url)
geo_data = geo_request.json()
org=geo_data["organization"] #https://get.geojs.io sitesinden Org (organization) değeri çekiliyor.
neworg=org.replace(" ","_") #organization değeri içerisindeki boşluk (" ") değerlerinin yerine "_" ifadesi yazılıyor ve neworg değişkenine atılıyor. Yazılma nedeni dosya içinde bu değerin bir bütün olarak görülmesini istiyoruz. Aksi halde organization değerini data.txt dosya içerisinde parse edemiyor.
print ('Temp: '+ str(temp) + '*C' + '\tHumidity:' + ' %'+ str(hum) + ' ' + str(time.strftime("%s",time.gmtime()))) #Sensörden aldığımız değerleri ekrana yazdırıyoruz.
data.write('temperature,location=' + neworg + ' temp='+ str(temp)) #data.txt dosyasının içerisine verileri yazıyoruz.
data.write('\n')
data.write('temperature,location=' + neworg +  ' hum='+ str(hum)) #data.txt dosyasının içerisine verileri yazıyoruz.

#Mail gönderme formatı
def mail(content):
    mail = smtplib.SMTP("smtp.gmail.com",587) 
    mail.starttls()
    mail.login('youremail@gmail.com','password')
    mail.sendmail("youremail@gmail.com","targetemail@gmail.com",content)

#content değişkenine uyarı mesajları atıldı ve mail fonksiyonu content parametresi ile çağrıldı.
if temp>=25.0:
    content = 'Oda sicakligi ' + str(temp) + '*C' + ' Sicaklik yuksek!'
    mail(content)
elif temp<=15.0:
    content = 'Oda sicakligi ' + str(temp) + '*C' + ' Sicakligi artirmaniz onerilir.'
    mail(content)
elif hum >=35.0:
    content = 'Odadaki nem orani  %' +  str(hum)  + ' Nem orani cok yuksek!'
    mail(content)
elif hum <=15.0:
    content = 'Odadaki nem orani  %' +  str(hum)  + ' Nem orani cok dusuk!'
    mail(content)
