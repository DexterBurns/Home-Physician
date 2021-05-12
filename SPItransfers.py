import spidev
importy RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

#device 0 which should be me and Ami's ESP-32
spi0 = spidev.SpiDev()
spi0.open(0,0) #Should be Header Pin 24 (GPIO 8 pink??)
spi0.max_speed_hz = 61000 #max speed is 61Khz

aba = 1
bp = 0x0001

Pi2ESP = 5
ESP2Pi = 6

int dataReceived = 0

#handshake pin from pi -> esp32
GPIO.setup(Pi2ESP, GPIO.OUT)

#handshake pin from esp32 -> pi
GPIO.setup(ESP2Pi, GPIO.IN)




#Steps: remember, only master can initiate communications
#Have the pi start up the SPI bus and pull the chip select line high, might need handshake pins (2 of em, one for esp32 to pi and for pi to esp32) so the ESP32 can let the pi know that it is ready.
#Pi will send a bitcode to the ESP32, this bitcode will tell the esp32 which fucntion to perform
#Once the bitcode has been sent, the pi will stop the SPI bus and the ESP32 will take the bitcode and peform which function the bitcode defines. ESP32 might need to tell pi it got the bitcode

#ESP32, once it has finished performing the bitcode function, will send handshake signal to the Pi to start up the SPI bus again.
#ESP32 will then forward bits over the MISO line to the Pi
#Pi will then read those bits from the buffer (which should be the results of the function performed by the ESP32)
#Pi will display the results to the user and then store it intot the database


espCheck():
    #make Pi to ESP handshake pin high (will be GPIO 5 or pin #29)
    GPIO.output(Pi2ESP, 1)
    
    signalReceived = 0
    
    #keep checking for the signal from the esp32, will wait on response from esp32
    while(signalReceived == 0):
        signalReceived = GPIO.input(ESP2Pi)
    
    #lower the Pi to ESP pin after the signal from ESP32 has been received
    GPIO.output(Pi2ESP, 0)
    #have the esp32 lower it's handshake pin as well

espDone():
    
    #waiting on the handhake signal from ESP32 saying that it will pump out bytes back to the pi
    while(GPIO.input(ESP2Pi) == 0):
        pass
    
    #reading the byte of data sent from the esp32, may only need one, for now
    dataReceived = readbytes(1)

    #make sure esp32 deasserts its ready line at this point, so the code doesnt think the esp32 is always ready

#main function
while aba == 1 :
    
    #function to check if esp32 is ready for input
    espCheck()
    
    #when esp32 is ready for input, send over the bitcode
    #esp32 should be in a state to receive bits from pi at this point
    spi0.xfer2(bp)
    
    
    
    #function that will wait on response from ESP32 saying that the ESP32 is done doing what it is supposed to
    #espDone()
    