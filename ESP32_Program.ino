#include <WireCrc.h>
#include <WirePacker.h>
#include <WireSlave.h>
#include <WireSlaveRequest.h>
#include <WireUnpacker.h>
#include "Arduino.h"
#include <Wire.h>

#include <PeakDetection.h>
#include "Arduino.h"
#include <Smoothed.h>

//related communication pins
#define SDA_PIN 21
#define SCL_PIN 22
#define I2C_SLAVE_ADDR 0x08
#define Pi2ESP 34 //pin 26 on pi
#define ESP2Pi 32 //pin 6 on pi

//related blood pressure pins
#define PTI 25 //output directly from the pressure transducer
#define FPTI 27 //filtered output from the pressure transducer
#define SCHMITT 26 //schmitt trigger output
#define MOTOR 19 //BP motor start/stop
#define LATCH 4//Latch to trap air


//initilizing library objects
PeakDetection peakDetection;
Smoothed <double> pressureTrans;

//iniitializing command variable and sending variable for communications
char command = 'A';
int sendValue = 0;

//related blood pressure variables
bool start = true;
bool timer = true;
long previousMillis = 0;
unsigned long currentMillis = 0;
long interval = 20000;
int doot = 0;
double meanMax = 0;
double meanPressure = 0;

void setup() {

  Serial.begin(115200);
  //communication setups
  bool success = WireSlave.begin(SDA_PIN, SCL_PIN, I2C_SLAVE_ADDR);
    if (!success) {
        Serial.println("I2C slave init failed");
        while(1) delay(100);
    }
    
  // Call receiveEvent when data received                
  WireSlave.onReceive(receiveEvent);
  // Call requestEvent when data requested
  WireSlave.onRequest(requestEvent);

  //blood pressure setups
  pinMode(PTI, INPUT);
  pinMode(FPTI, INPUT);
  pinMode(SCHMITT, INPUT);
  pinMode(MOTOR, OUTPUT);
  pinMode(LATCH, OUTPUT);
  peakDetection.begin(200, 0.8, 0.01);
  previousMillis = millis();
  pressureTrans.begin(SMOOTHED_AVERAGE, 10);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  //have the esp32 wait until it receives a signal from the pi
  //will keep polling communication lines for a signal from pi
  WireSlave.update();
  delay(1);

  //if command is a, do nothing,
  //if command is b, take blood pressure,
  //if command is c, take pulse oximetry,
  //if command is d, take temperature
  //set the command letter in the receiveEvent function
  //Add code to the functions as necessary, blood pressure monitor is called when it receives 'B' from the Pi

  /*
  switch (command) {
    case 'a':
    //do nothing
      break;
    case 'b':
      bloodPressure();
      command = 'a';
      start = true;
      break;
    case 'c':
      //pulseOximeter();
      command = 'a';
      break;
    case 'd':
      //takeTemperature();
      command = 'a';
      break;
    default:
      command = 'a';
      break;
    
  }*/

  if (command == 'A')
  {
    ;//do nothing
  }

  else if(command == 'B')
  {
    bloodPressure();
    command = 'A';
    start = true;
  }

  else if(command == 'C')
  {
    //pulseOximeter();
      command = 'A';
  }

  else if(command == 'D')
  {
    //takeTemperature();
      command = 'A';
  }

  else
  {
    command = 'A';
  }

  WireSlave.update();
  delay(1);
}

void receiveEvent(int howMany) {
  while (WireSlave.available()) { // loop through all but the last
    char received = WireSlave.read(); // receive byte as a character
    //set command char here
    command = received;
    Serial.print("data received: ");
    Serial.println(received);
  }
}


void requestEvent()
{
    //make sure other functions change sendValue to the appropriate value!!!
    Serial.print("data sent: ");
    Serial.println(sendValue);
    WireSlave.write(sendValue);
  
}

/////////////////////////
//blood pressure functions
////////////////////////
void bloodPressure()
{
    //inflate to full size
    //hold there for about 5 seconds
    //then start deflating
    if(start == true)
    {
       turnOn();
    }
    
    //inflating until at max pressure
    while(analogRead(PTI) <= 2900 && start == true)
    {
      //starting the bp machine
      
      //Serial.print("PTI here: ");
      //Serial.println(analogRead(PTI));
      previousMillis = millis();
  
      if(digitalRead(SCHMITT) == LOW)
      {
        while(1)
        {
          Serial.print("Schmitt read low");
          turnOff();
        }
      }
    }
  
    turnOffMotor();
  
    if(start == true)
    {
      airHold();
    }
    
    start = false;
}

void airHold()
{
  //function that will record the held pressure in the cuff for 5 seconds
  previousMillis = currentMillis = millis();

  //Serial.println("Air Holding");
  
  do{
    pressureTrans.add(analogRead(PTI));
    double smoothed = pressureTrans.get();
    double mydata = smoothed/1500-1; // reads the value of the sensor and converts to a range between -1 and 1
    peakDetection.add(mydata); // adds a new data point
    int peak = peakDetection.getPeak(); // returns 0, 1 or -1
    double filtered = peakDetection.getFilt(); // moving average
    Serial.print(mydata); //print data
    Serial.print(",");
    Serial.print(peak); //print peak status
    Serial.print(",");
    Serial.println(filtered); //print moving average
    currentMillis = millis();
    //Serial.print(",");
    //Serial.println(analogRead(FPTI));

    //finding the mean arterial pressure here
    if(meanMax < analogRead(FPTI))
    {
      meanMax = analogRead(FPTI);
      meanPressure = analogRead(PTI);
    }
    
    //safety measure, will shut off circuit when schmitt trigger reads low
    if(digitalRead(SCHMITT) == LOW)
    {
      while(1)
      {
        Serial.print("Schmitt read low");
        turnOff();
      }
    }
    
  }
  
  while( (currentMillis - previousMillis) < interval );

  digitalWrite(LATCH, LOW);

  Serial.print("Mean Arterial P: ");
  Serial.println(meanPressure);
  
  double systolic = (0.7*meanPressure);
  double diastolic = (0.5*meanPressure);

  double mmMean = map(meanPressure, 0, 4000, 0, 200);
  double mmSystolic = map(systolic, 0, 4000, 0, 200);
  double mmDiastolic = map(diastolic, 0, 4000, 0, 200);

  Serial.print("Mean Pressure: ");
  Serial.println(mmMean);
  Serial.print("Systolic Pressure: ");
  Serial.println(mmSystolic);
  Serial.print("Diastolic Pressure ");
  Serial.println(mmDiastolic);
  
  
}

void turnOn()
{
  digitalWrite(MOTOR, HIGH);
  digitalWrite(LATCH, HIGH);
}

void turnOff()
{
  digitalWrite(MOTOR, LOW);
  digitalWrite(LATCH, LOW);
}

void turnOffMotor()
{
  digitalWrite(MOTOR, LOW);
  
}

/////////////////////////
///Pulse Oximeter Code
////////////////////////
