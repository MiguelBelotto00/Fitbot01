#importando las librerias que utilizaremos
import random
import time
import tweepy
import schedule
from tweepy import Status

#importar configuraciones de twitter
from botfit_config import consumer_key,consumer_secret,access_token,access_token_secret


#conexion con twitter apps , inicio de sesion en Api y en twitter
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

#Funcion para saber porcentaje de fit al azar
def fitporcent():
     num=float(100)
     num2=random.randint(1,100)
     num3=random.randint(1,100)
     porcent=(num2*num3)/num
     fitness= int(porcent)
     return fitness
impresion = fitporcent()
#Funcion para Twittear, y lo que queremos que twittee.
def twittear():
 api.update_status(status="hora de entrenar")

#Definimos la funcion, para la hora de twitteo y para respuesta. En mi caso seran todos los dias a las 7:00am y 17:00pm y las respuesta las verifica cada 10 segundos
def main():
     schedule.every(7).seconds.do(check_mentions)
     # schedule.every().day.at('12:00').do(twittear)
     # schedule.every().day.at('20:00').do(twittear)
     while True:
	     try:
		     schedule.run_pending()
		     time.sleep(2)
	     except tweepy.TweepError as e:
	          raise e
    
#Almacenamiento de la id de una mencion
def almacenamientoid(id):
     file = open('last_id.txt', 'w')
     file.write(str(id))
     file.close()
#Lectura de id para menciones del bot
def leer_ultimaid():
     file = open('last_id.txt', 'r')
     id = int(file.read().strip())
     file.close()
     return id
#Definicion para responder menciones
def check_mentions():
     menciones=api.mentions_timeline(leer_ultimaid(),tweet_mode = 'extended')
     for tweet in reversed(menciones):
         print(tweet.full_text)
         respuesta(tweet)

#Respuesta del tweet
def respuesta(tweet):
     api.update_status("@"+tweet.user.screen_name+' sos '+str(impresion)+" % musculoso", tweet.id)
     almacenamientoid(tweet.id)

#Definicion del main
if __name__=="__main__":
     main()
