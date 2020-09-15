import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from datetime import datetime
import time
GPIO.setmode(GPIO.BCM)

LCD_RS    = 27
LCD_E     = 22
LCD_D4    = 24
LCD_D5    = 25
LCD_D6    = 4
LCD_D7    = 17

door=16
alarma=20
indic=19

HoraInicio="00:00"
HoraFinal="00:00"

Ab_Up= 5
Ce_Do= 6
H_INI= 12
H_FIN= 13
act=26
desc=21

activa=0
# DEFINIR CONSTANTES DEL DISPOSITIVO
LCD_WIDTH = 32 # CARACTERES MAXIMOS POR FILA
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # DIRECCION RAM PARA PRIMERA LINEA
LCD_LINE_2 = 0xC0 # DIRECCION RAM PARA SEGUNDA LINEA
E_PULSE = 0.00005 # CONSTANTES PARA RETARDOS
E_DELAY = 0.00005

def on_message(client,obj,msg):
    Datos=msg.payload.decode('utf-8')
    actualizarVariables(Datos)

def actualizarVariables(dat):
    global activa,HoraFinal,HoraInicio
    vars=dat.split(";")
    if(vars[0]=="Hfin"):
        HoraFinal=vars[1]
    if(vars[0]=="Hini"):
        HoraInicio=vars[1]
    if(vars[0]=="activa"):
        activa=int(vars[1])
        if(activa==1):
            GPIO.output(indic,1)
            Puerta(180)
        if(activa==0):
            GPIO.output(indic,0)
            Puerta(100)
            GPIO.output(alarma,0)
    if(vars[0]=="abrir"):
        if(vars[1]=="1"):
            Puerta(100)
            if(activa==1):
                GPIO.output(alarma,1)
        if(vars[1]=="0"):
            Puerta(180)
            GPIO.output(alarma,0)


def Puerta(val):
        pwm=GPIO.PWM(door,100)
        pwm.start((val)/10.+5.)
        time.sleep(0.2)
        pwm.stop()

def main():
    global HoraInicio,HoraFinal,activa
    mqttc=mqtt.Client()
    mqttc.on_message=on_message
    mqttc.username_pw_set("patriciabonilla1995@gmail.com","1726646654")
    mqttc.connect("maqiatto.com",1883)
    mqttc.subscribe("patriciabonilla1995@gmail.com/test1",0)
     # DEFINIR GPIO COMO SALIDA PARA USAR LA LCD
    GPIO.setup(LCD_E, GPIO.OUT) # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
     # INICIALIZAR DISPLAY
    lcd_init()
    time.sleep(1)


    GPIO.setup(Ab_Up,GPIO.IN)
    GPIO.setup(Ce_Do,GPIO.IN)
    GPIO.setup(H_INI,GPIO.IN)
    GPIO.setup(H_FIN,GPIO.IN)
    GPIO.setup(act,GPIO.IN)
    GPIO.setup(desc,GPIO.IN)
    GPIO.setup(door,GPIO.OUT)
    GPIO.setup(alarma,GPIO.OUT)
    GPIO.setup(indic,GPIO.OUT)
    
    Hact=""

    while(1):
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("       Alarma temporizada")
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("Encendido  "+HoraInicio+"  Apagado  "+HoraFinal)
        Hact =time.strftime("%H:%M:%S")
        mqttc.loop()
        if(GPIO.input(Ab_Up)==0):
           Puerta(100)
           if(activa==1):
               GPIO.output(alarma,1)

        if(GPIO.input(Ce_Do)==0):
            Puerta(180)
            GPIO.output(alarma,0)

        if(GPIO.input(H_INI)==0):
            ConfHora(0)

        if(GPIO.input(H_FIN)==0):
            ConfHora(1)

        if(GPIO.input(act)==0):
           GPIO.output(indic,1)
           activa=1
           Puerta(180)

        if(GPIO.input(desc)==0):
            GPIO.output(indic,0)
            activa=0
            Puerta(100)
            GPIO.output(alarma,0)

        if(Hact==HoraInicio+":00"):
            activa=1
            GPIO.output(indic,1)
            Puerta(180)

        if(Hact==HoraFinal+":00"):
            activa=0
            GPIO.output(indic,0)
            GPIO.output(alarma,0)
            Puerta(100)

        #mqttc.publish("patriciabonilla1995@gmail.com/test","dispositivo")
      

def ConfHora(control):
    global HoraInicio,HoraFinal
    time.sleep(0.5)
    if(control==0):
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(">Encendido  "+HoraInicio+"  Apagado  "+HoraFinal)
    else:
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("Encendido  "+HoraInicio+" >Apagado  "+HoraFinal)
    StrH="00"
    StrM="00"
    i=0
    CnTime=0
    while(1):
        if(GPIO.input(Ab_Up)==0):
            time.sleep(0.5)
            i=1+i
            if(CnTime==0):
                if(i>23):
                    i=0
            if(CnTime==1):
                if(i>59):
                    i=0
        if(GPIO.input(Ce_Do)==0):
            time.sleep(0.5)
            i=i-1
            if(CnTime==0):
                if(i<0):
                    i=23
            if(CnTime==1):
                if(i<0):
                    i=59
        if(control==0):
            if(GPIO.input(H_INI)==0):
                time.sleep(0.5)
                CnTime=CnTime+1
                i=0
                if(CnTime==2):
                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    lcd_string("       Alarma temporizada")
                    lcd_byte(LCD_LINE_2, LCD_CMD)
                    lcd_string("Encendido  "+HoraInicio+"  Apagado  "+HoraFinal)
                    break
        if(control==1):
            if(GPIO.input(H_FIN)==0):
                time.sleep(0.5)
                CnTime=CnTime+1
                i=0
                if(CnTime==2):
                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    lcd_string("       Alarma temporizada")
                    lcd_byte(LCD_LINE_2, LCD_CMD)
                    lcd_string("Encendido  "+HoraInicio+"  Apagado  "+HoraFinal)
                    break
        if(control==0):        
            if(CnTime==0):
                if(i<10):
                    StrH="0"+str(i)
                else:
                    StrH=str(i)
            if(CnTime==1):
                if(i<10):
                    StrM="0"+str(i)
                else:
                    StrM=str(i)
            HoraInicio=StrH+":"+StrM
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string(">Encendido  "+HoraInicio+"  Apagado  "+HoraFinal)
        if(control==1):        
            if(CnTime==0):
                if(i<10):
                    StrH="0"+str(i)
                else:
                    StrH=str(i)
            if(CnTime==1):
                if(i<10):
                    StrM="0"+str(i)
                else:
                    StrM=str(i)
            HoraFinal=StrH+":"+StrM
            lcd_byte(LCD_LINE_2, LCD_CMD)
            lcd_string("Encendido  "+HoraInicio+" >Apagado  "+HoraFinal)
        
            
        
        

def lcd_init():													
    # PROCESO DE INICIALIZACION								
    lcd_byte(0x33,LCD_CMD)										
    lcd_byte(0x32,LCD_CMD)										
    lcd_byte(0x28,LCD_CMD)										
    lcd_byte(0x0C,LCD_CMD)											
    lcd_byte(0x06,LCD_CMD)										
    lcd_byte(0x01,LCD_CMD)										

def lcd_string(message):											
    # ENVIAR UN STRING A LA LCD								
    message = message.ljust(LCD_WIDTH," ")						
    for i in range(LCD_WIDTH):										
        lcd_byte(ord(message[i]),LCD_CHR)							

def lcd_byte(bits, mode):														
    GPIO.output(LCD_RS, mode) # RS											
    GPIO.output(LCD_D4, False)									
    GPIO.output(LCD_D5, False)									
    GPIO.output(LCD_D6, False)									
    GPIO.output(LCD_D7, False)									
    if bits&0x10==0x10:												
        GPIO.output(LCD_D4, True)									
    if bits&0x20==0x20:											
        GPIO.output(LCD_D5, True)									
    if bits&0x40==0x40:											
        GPIO.output(LCD_D6, True)									
    if bits&0x80==0x80:											
        GPIO.output(LCD_D7, True)									
    time.sleep(E_DELAY)														
    GPIO.output(LCD_E, True)										
    time.sleep(E_PULSE)											
    GPIO.output(LCD_E, False)										
    time.sleep(E_DELAY)															
    GPIO.output(LCD_D4, False)								
    GPIO.output(LCD_D5, False)									
    GPIO.output(LCD_D6, False)									
    GPIO.output(LCD_D7, False)									
    if bits&0x01==0x01:											
        GPIO.output(LCD_D4, True)									
    if bits&0x02==0x02:											
        GPIO.output(LCD_D5, True)										
    if bits&0x04==0x04:											
        GPIO.output(LCD_D6, True)									
    if bits&0x08==0x08:											
        GPIO.output(LCD_D7, True)									
    time.sleep(E_DELAY)											
    GPIO.output(LCD_E, True)										
    time.sleep(E_PULSE)											
    GPIO.output(LCD_E, False)										
    time.sleep(E_DELAY)			