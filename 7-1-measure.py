import RPi.GPIO as GPIO
import time as t
import matplotlib.pyplot as plt

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds=[21,20,16,12,7,8,25,24]
comp = 4
vertel = 17

vt=[]
st=t.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(vertel, GPIO.OUT, initial = 0)

def binarize(number):
    return [int(i) for i in bin(number)[2:].zfill(8)]

def adc_sar():
    value=127
    for i in range(-6,1):
        i=-i
        GPIO.output(dac,binarize(value))

        t.sleep(0.001)
        
        if GPIO.input(comp):value+=(2**i)
        else:value+=-(2**i)
    
    return value

def led_ind(value):
    GPIO.output(leds,binarize(value))
    
try:
    GPIO.output(vertel,1)
    mes=0                                                                                                                                 
    while mes<220:
        mes=adc_sar()
        print(mes)
        vt.append(mes)
        led_ind(mes)
    GPIO.output(vertel,0)
    print('pазрядка')
    GPIO.output(vertel, 0)
    GPIO.output(dac, binarize(0))

    discharge_measerments = []
    while adc_sar()>100:
        discharge_measerments.append(adc_sar())
        t.sleep(0.001)
        
        
except KeyboardInterrupt:
    pass

finally:
    GPIO.output(vertel,GPIO.LOW)
    GPIO.output(dac,GPIO.LOW)
    GPIO.cleanup()

vts=""
for i in vt:
    vts=vts+(str(i)+"\n")

with open("data.txt","w") as data:
    data.write(vts)
with open("settings.txt","w") as data:
    data.write("Freq=1000, Step=13")
    
print('Общая продолжительность эксперимента: '+str(t.time()-st)+"c")
print("период одного измерения: 5мс")

    
plt.plot([i for i in range(0,len(vt))],[(i/255)*3.3 for i in vt],c="blue")
plt.grid()
plt.show()