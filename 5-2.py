import RPi.GPIO as GPIO
import time


dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13


GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

GPIO.setup(troyka, GPIO.OUT, initial=1)

GPIO.setup(comp, GPIO.IN)

def decimal_to_binary_list(n):
    return [int(bit) for bit in bin(n)[2:].zfill(8)]

def adc():
    value = 0
    for i in range(7,-1,-1):  
        value +=2**i
        GPIO.output(dac, decimal_to_binary_list(value))
        #print(value)
        time.sleep(0.005) 
        if GPIO.input(comp) == 1:
            value -=2**i
    return value

try:
    while True:
        value = adc()  
        voltage = (value / 256.0) * 3.3 
        print(f" {voltage:.2f}V")
finally:
    GPIO.output(dac, 0)
    
    GPIO.cleanup()