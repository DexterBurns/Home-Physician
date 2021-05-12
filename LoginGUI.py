#continuation notes
#Just trying to learn how SPI between our Pi and ESP-32 gonna work, because before i implement it into
#the gui, i need to know what its capapble of


#Manual code for the login GUI

#relevant GUI imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from picamera import PiCamera
import time
from time import sleep

import random

#relevant database imports
from PyQt5.QtSql import QSqlDatabase
import sqlite3
import spidev

#device 0 which should be me and Ami's ESP-32
spi0 = spidev.SpiDev()
spi0.open(0,0) #Should be Header Pin 24 (GPIO 10 pink)
spi0.max_speed_hz = 61000 #max speed is 61Khz

#device 1 which should be Dame's ESP-32
spi1 = spidev.SpiDev()
spi1.open(0,1) #should be header pin 26 (GPIO 11 pink)
spi1.max_speed_hz = 61000 #61khz max speed

#import matplotlib plot elements
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
import matplotlib.pyplot as plt4
import matplotlib.pyplot as plt5

userName = "Dexter238"
passWord = "N/a"

userTrue = 0
passTrue = 0


#camera = PiCamera()


global actualUserName
global newUserPin
global newUserHeight
global newUserSex
global newUserDOB

global addedUser
global userProfileVariables
global timer

#creating the database for storing user information
path = "/home/pi/HomePhysicianDatabase.db"
print ("Database opened.")
       
#creating a connection object 
conn = sqlite3.connect(path)

'''
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA

def changeExposure(exposureSelection):
    # exposure selection should include off, auto, night, backlight
    
    camera.exposure_mode = exposureSelection
    if camera.exposure_mode == 'off':
        changeIso(100)
        changeShutter(100)

def changeIso(isoNumber):
    #ISO values should be 100, 200, 300, ... ,800
    camera.iso = isoNumber
                              
def changeShutter(shutterNumber):
    #Shutter values should be 1/250, 1/125, 1/60, 1/30, 1/15, 1/8,
    #1/4, 1/2, 1') the shutter is in ms, 20000 is equal to 20ms
    # should be formatted as 20000 for input;
    camera.shutter_speed = shutterNumber

def changeAWB(awbSelection):
    #white balance selection include: off, auto, tungsten, flourescent
    #incandescent, sun, cloud..
    camera.awb_mode = awbSelection

#if GPIO detects high, take image
def takePicture(pictureType):
    #pictureType should be the delay in seconds, 0 = single fire, 3 = 3 sec.. selections: 0,3,5,10
    #delay function
    time = setTimer()
    delay(time)
    camera.capture("%d-%m-%Y-%H:%M.jpg")
    
    
def setTimer(time):
    global timer
    timer = time
    return timer
    

#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
#CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA CAMERA
'''


#all database functions will be defined starting from here
def storeBloodPressure(conn, bpReading):
    sql = ''' INSERT INTO BPREADINGS(user_id,systolic,diastolic,meanarterialpressure,bp_date)
              VALUES (?,?,?,?,?) '''
    cur = conn.cursor()
    
    cur.execute(sql,bpReading)
    conn.commit()

def getBloodPressure():
    global conn
    global userName
    
    sql = 'SELECT systolic, diastolic, meanarterialpressure, bp_date FROM BPREADINGS WHERE user_id = ? ORDER BY date(bp_date) ASC Limit 30'
    cur = conn.cursor()
    
    cur.execute(sql, (userName,))
    
    bpData = cur.fetchall()
    print(bpData)
    
    return bpData
    
#getBloodPressure()    

def plotBloodPressure():
    
    #list of tuples that we get from database
    pressureData = getBloodPressure()
    
    systolic = []
    diastolic = []
    meanarterial = []
    bpDate = []
    
    ##trying to access the individual data in the tuples: this is called list comprehension
    systolic = [lis[0] for lis in pressureData]
    diastolic = [lis[1] for lis in pressureData]
    meanarterial = [lis[2] for lis in pressureData]
    bpDate = [lis[3] for lis in pressureData]
        
    print(systolic)
    print(diastolic)
    print(meanarterial)
    print(bpDate)
    
    plt1.plot(bpDate,systolic, 'bo', label="Systolic")
    plt1.plot(bpDate,diastolic, 'r+', label = "Diastolic")
    plt1.plot(bpDate,meanarterial, 'mx', label = "Mean Arterial Pressure")
    plt1.legend()
    plt1.xticks(rotation=45, ha="right")
    plt1.rc('font', size=3)
    plt1.show()
       
#plotBloodPressure()

def storeBloodOxygen(conn, boReading):
    sql = '''INSERT INTO BLOODOXREADINGS(user_id, blood_ox, blood_ox_date)
            VALUES (?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (boReading,))
    conn.commit()

def getBloodOxygen():
    global conn
    global userName
    
    sql = 'SELECT blood_ox, blood_ox_date FROM BLOODOXREADINGS WHERE user_id = ? ORDER BY date(blood_ox_date) DESC Limit 30'
    cur = conn.cursor()
    
    cur.execute(sql, (userName,))
    
    Data = cur.fetchall()
    print(Data)
    
    return Data

def plotBloodOxygen():
    
    bloodOxData = getBloodOxygen()
    
    oxygenLevel = []
    oxygenDate = []
    
    oxygenLevel = [lis[0] for lis in bloodOxData]
    oxygenDate = [lis[1] for lis in bloodOxData]
    
    pl2.plot(oxygenDate,oxygenLevel, 'b-', label = "Blood Oxygen Level (of %100)")
    pl2.legend()
    plt2.xticks(rotation=45, ha="right")
    plt2.show()

def storePupillometer(conn, pupilReading):
    sql = '''INSERT INTO PUPILLOMETER(user_id, constrict_time, pupil_date)
            VALUES (?,?,?) '''
    
    cur = conn.cursor()
    cur.execute(sql,pupilReading)
    conn.commit()

def getPupillometer():
    global conn
    global userName
    
    sql = 'SELECT constrict_time, pupil_date FROM PUPILLOMETER WHERE user_id = ? ORDER BY date(pupil_date) DESC Limit 30'
    cur = conn.cursor()
    
    cur.execute(sql, (userName,))
    
    Data = cur.fetchall()
    print(Data)
    
    return Data

def plotPupillometer():
    
    pupilData = getPupillometer()
    dilationTime = []
    dilationDate = []
    dilationTime = [lis[0] for lis in pupilData]
    dilationDate = [lis[1] for lis in pupilData]
    pl3.plot(dilationDate,dilationTime, 'b-', label = "Dilation Time (millisecs)")
    pl3.legend()
    pl3.xticks(rotation=45, ha="right")
    pl3.show()

def storeTempReadings(conn, tempReading):
    sql = '''INSERT INTO TEMPREADINGS(user_id, c_temp, f_temp, temp_date)
            VALUES (?,?,?,?) '''
    
    cur = conn.cursor()
    cur.execute(sql,tempReading)
    conn.commit()

def getTempReadings():
    global conn
    global userName
    
    sql = 'SELECT c_temp, f_temp, temp_date FROM TEMPREADINGS WHERE user_id = ? ORDER BY date(temp_date) DESC Limit 30'
    cur = conn.cursor()
    
    cur.execute(sql, (userName,))
    
    Data = cur.fetchall()
    print(Data)
    
    return Data

def plotTempReadings():
    tempData = getTempReadings()
    f_Temperature = []
    c_Temperature = []
    temp_Date = []
    c_Temperature = [lis[0] for lis in tempData]
    f_Temperature = [lis[1] for lis in tempData]
    temp_Date = [lis[2] for lis in tempData]
    plt4.plot(temp_Date,c_Temperature, 'b-', label = "Celsius Temperature")
    plt4.plot(temp_Date,f_Temperature, 'r-', label = "Fahrenheit")
    plt4.legend()
    plt4.xticks(rotation = 45, ha = "right")
    plt4.legend()
    plt4.show()
    

def storeWeightReadings(conn, weightReading):
    sql = '''INSERT INTO WEIGHTREADINGS(user_id,weight_lbs,weight_kgs,weight_date)
            VALUES (?,?,?,?) '''
    
    cur = conn.cursor()
    cur.execute(sql,weightReading)
    conn.commit()

def getWeightReadings():
    global conn
    global userName
    
    sql = 'SELECT weight_lbs, weight_kgs, weight_date FROM TEMPREADINGS WHERE user_id = ? ORDER BY date(weight_date) DESC Limit 30'
    cur = conn.cursor()
    
    cur.execute(sql, (userName,))
    
    Data = cur.fetchall()
    print(Data)
    
    return Data

def plotWeightReadings():
    weightData = getWeightReadings()
    lbs_Weight = []
    kgs_Weight = []
    date_Weight = []
    lbs_Weight = [lis[0] for lis in weightData]
    kgs_Weight = [lis[1] for lis in weightData]
    date_Weight = [lis[2] for lis in weightData]
    plt5.plot(date_Weight,lbs_Weight, 'b-', label = "Weight in lbs")
    plt5.plot(date_Weight,kgs_Weight, 'r-', label = "Weight in kilos")
    plt5.xticks(rotation = 45, ha = "right")
    plt5.legend()
    plt5.show()
    

def storeNewUser(conn, newUser):
    sql = '''INSERT INTO USERS(user_id, pin_num)
            VALUES (?,?)'''
    
    cur = conn.cursor()
    cur.execute(sql,newUser)
    conn.commit()

def storeUserInfo(conn, userInfo):
    sql = ''' INSERT INTO USERINFO(user_id, user_name, user_height, user_sex, user_dob)
            VALUES (?,?,?,?,?)'''
    
    cur = conn.cursor()
    cur.execute(sql,userInfo)
    conn.commit()

def getUserInfo():
    sql = 'SELECT user_id, user_name, user_height, user_sex, user_dob FROM USERINFO WHERE user_id = ?'
    cur = conn.cursor()
    cur.execute(sql, (userName,))
    
    userData = cur.fetchone()
    return userData
       
#issue: for some reason actualUserName is not defined????
def generateUserId(actualUserName):
    #getting the first name of the user 
    splitName = actualUserName.split()[0]
    
    randId1, randId2, randId3 = random.sample(range(1, 9), 3)
    randstr1 = str(randId1)
    randstr2 = str(randId2)
    randstr3 = str(randId3)
    
    global userName 
    userName = splitName + randstr1 + randstr2 + randstr3
    #return userName
    #userName IS THE USER ID OF THE PERSON EG: DEXTER1234, actualUserName is the ACTUAL name of the person eg; Dexter Burns, wouldve done this differently but too late to change

def userChecker():
    
    global userName
    global passWord
    
    userName = userEntry.text()
    passWord = passEntry.text()
    
    testFunc()
    
    #checks if the user exists in the database
    sql = '''SELECT user_id FROM USERS WHERE user_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (userName,))
    data1 = cur.fetchone()
    
    if data1 is None:  
        userTrue = 0
        print("UserTrue = 0")
        
    else:
        userTrue = 1
        print("UserTrue = 1")
        
        
    sql2 = 'SELECT user_id FROM USERS WHERE pin_num = ?'
    cur2 = conn.cursor()
    cur2.execute(sql2, (passWord,))
    
    if cur2.fetchone():
        passTrue = 1
        print("PassTrue = 1")
    else:
        passTrue = 0
        print("PassTrue = 0")
    
    if userTrue == 1 and passTrue == 1:
        clearLoginScreen()
        showMainButtons()
    
def userInstructions(code):
    
    #This will be used to pop up a window giving the user instructions and a button to start whichever process
    ##note: Doing instructional popup window to give instructions to the user on how to perform the given part of the project
    #Label.clear() to delete the text of a label
    #dont forget to SHOW the insWindow
    
    camCombo.hide()
    whiteCombo.hide()
    isoSlider.hide()
    shutterSlider.hide()
    takePic.hide()
    insStartButton.show()
    '''
    camera.close()
    '''
    
    insWindow.show()
    if code == "BloodPressure":
        insMessage.clear()
        hexCode = 0x0001
        insMessage.setPlainText("How to use the Blood Pressure Monitor:\n1.Place your left arm into the cuff.\n2.Pull the strap until the cuff lightly squeezes your arm.\n3.Orient the cuff so that the artery mark on the cuff is aligned with your bicep.\n4.Once the above steps are done, click the 'Start' button to begin.")
        
    elif code == "BloodOxygen":
        insMessage.clear()
        hexCode = 0x0010
        insMessage.setPlainText("How to use the Blood Oxygen Sensor:\n1.Place your left index finger snug into the Blood Oxygen sensor module.\n2.Once your finger is placed, click the 'Start' buttn to begin the test")
        
    elif code == "Weight":
        insMessage.clear()
        hexCode = 0x0100
        insMessage.setPlainText("How to use the Scale:\n1.Pull the scale out from its compartment and place it on the ground.\n2.Stand on the scale and stand still.\n3.Press the start button when you are ready to take your weight.")
        
    elif code == "Temperature":
        insMessage.clear()
        hexCode = 0x1000
        insMessage.setPlainText("How to take your temperature:\n1.Bring the temperature sensor unit to your forehead\n2.Keep it to your forehead and press the start button to take your temperature")
        
    elif code == "Pupillometer":
        #probably needs to link to Dame's function for controlling the pupillometer
        insMessage.clear()
        hexCode = 0x0011
        insMessage.setPlainText("How to use the Pupillometer:\n1.Click the start button when you are ready to begin the pupillometer test.\nYou will have 5 seconds to look into the eye-slots before the Test Begins.\nMake sure not to blink!")
    
    elif code == "Ailments":
        insMessage.clear()
        hexCode = 0x0101
        insMessage.setPlainText("Please Enter any ailments and pains you have into this text box:")
    
    '''
    elif code == "Bodycam":
        insMessage.clear()
        hexCode = 0x1001
        insMessage.setPlainText("<---- Change Exposure Mode\n\n<----Change White Balance\n\n\n<----Change ISO\n\n<----Change Shutter")
        insStartButton.hide()
        camCombo.show()
        whiteCombo.show()
        isoSlider.show()
        shutterSlider.show()
        takePic.show()
        
        
        #starting up the camera
        camera.resolution = (1024, 768)
        camera.start_preview(fullscreen = False, window = (200, 200, 400, 400))
     '''   

        
    #make a button that sends a signal over spi to the ESP32 OOF DONT FORGET THE BODYCAM!!!!!!!!!!
    insMessage.show()

#creating a QApplication instance
app = QApplication(sys.argv)


#creating the GUI instance
window = QWidget()
window.setWindowTitle('Home Physician GUI')
window.setGeometry(0,0,0,0)
window.setFixedWidth(800)
window.setFixedHeight(480)
window.setStyleSheet("background-color: rgb(246,196,146)")

#creating 2nd GUI instance for sign up page
signUpWindow = QWidget()
signUpWindow.setWindowTitle('Sign Up Here!')
signUpWindow.setGeometry(0,0,800,480)
signUpWindow.setFixedWidth(800)
signUpWindow.setFixedHeight(480)
signUpWindow.setStyleSheet("background-color: rgb(246,196,146)")
signUpWindow.hide()

#creating a 3rd GUI instance for the instructional page
insWindow = QWidget()
insWindow.setWindowTitle("Please Read!!!")
insWindow.setFixedWidth(800)
insWindow.setFixedHeight(480)
insWindow.setStyleSheet("background-color: rgb(246,196,146)")
insWindow.hide()
insMessage = QTextEdit('Test Textdigbsjdgnbkjsnbg;skdjskjdbadjklbnjklbnjdfgdhgbdfjhgbdhgb', parent = insWindow)

#insMessage.setWordWrap(True)
insMessage.setGeometry(0,0, 300, 220)
insMessage.move(250, 100)
insMessage.show()
insStartButton = QPushButton("Start", parent = insWindow)
insStartButton.move(350,350)

#initializing ALL widgets below:
msg = QMessageBox()
msg.hide()


#creating the respective camera controls here(will probably be sliders)
#combobox to select exposure mode, goes in camGroup
camCombo = QComboBox()
camCombo.addItem("off")
camCombo.addItem("auto")
camCombo.addItem("night")
camCombo.addItem("backlight")
camCombo.setParent(insWindow)
camCombo.move(50,100)
camCombo.currentIndexChanged.connect(lambda:changeExposure(camCombo.currentText()))

#change white balance
whiteCombo = QComboBox()
whiteCombo.addItem("off")
whiteCombo.addItem("auto")
whiteCombo.addItem("tungsten")
whiteCombo.addItem("fluorescent")
whiteCombo.addItem("incandescent")
whiteCombo.setParent(insWindow)
whiteCombo.move(50,150)
#connect whitecombo to change white balance function
whiteCombo.currentIndexChanged.connect(lambda:changeAWB(whiteCombo.currentText()))

#slider to change iso and shutter, go in camgroupE
isoSlider = QSlider(Qt.Horizontal, parent = insWindow)
isoSlider.setMinimum(100)
isoSlider.setMaximum(800)
isoSlider.setTickInterval(100)
isoSlider.setTickPosition(QSlider.TicksBelow)
isoSlider.setParent(insWindow)
isoSlider.move(50, 200)
#connect iso slider to iso function
isoSlider.valueChanged.connect(lambda:changeIso(isoSlider.value()))

shutterSlider = QSlider(Qt.Horizontal, parent = insWindow)
shutterSlider.setMinimum(1/125)
shutterSlider.setMaximum(1)
shutterSlider.setTickInterval(.25)
shutterSlider.setTickPosition(QSlider.TicksBelow)
shutterSlider.setParent(insWindow)
shutterSlider.move(50,250)
#connect shutter slider to shutter function
shutterSlider.valueChanged.connect(lambda:changeShutter(shutterSlider.value()))

timerSlider = QSlider(Qt.Horizontal, parent = insWindow)
timerSlider.setMinimum(0)
timerSlider.setMaximum(5)
timerSlider.setTickInterval(1)
timerSlider.setTickPosition(QSlider.TicksBelow)
timerSlider.move(50, 300)
#connect slider to extra timer function in the camera section, take picture will grab the value it currently is
timerSlider.valueChanged.connect(lambda:setTimer(timerSlider.value()))

#take picture button
takePic = QPushButton('Take Picture', parent = insWindow)
takePic.move(50, 300)
takePic.clicked.connect(lambda:takePicture())

camCombo.hide()
whiteCombo.hide()
isoSlider.hide()
shutterSlider.hide()
takePic.hide()



#main page(will include functions so when these button are clicked, a window showing the instructions for the user to follow will appear)
#action to take on button clicked for stuff on the main page will be here too
logoutButton = QPushButton('Logout', parent = None)

PastDataButton = QPushButton('Past Data', parent = None)

bloodPressureButton = QPushButton('Blood Pressure', parent = None)
bloodPressureButton.clicked.connect(lambda:userInstructions("BloodPressure"))

pulseOximeterButton = QPushButton('Pulse Oximeter', parent = None)
pulseOximeterButton.clicked.connect(lambda:userInstructions("BloodOxygen"))

pupilDilationButton = QPushButton('Pupil Dilation', parent = None)
pupilDilationButton.clicked.connect(lambda:userInstructions("Pupillometer"))

bodyCameraButton = QPushButton('Bodycam', parent = None)
bodyCameraButton.clicked.connect(lambda:userInstructions("Bodycam"))
#Connect the bodyCameraButton to Dame's bodycam function

weightButton = QPushButton('Weight', parent = None)
weightButton.clicked.connect(lambda:userInstructions("Weight"))

bodyTempButton = QPushButton('Take Temperature', parent = None)
bodyTempButton.clicked.connect(lambda:userInstructions("Temperature"))

ailmentsAndPain = QPushButton('Ailments/Pain Entry', parent = None)
ailmentsAndPain.clicked.connect(lambda:userInstructions("Ailments"))

#need a text box showing the user information
displayUser = QTextEdit("", parent = window)
displayUser.hide()

#login page
welcomeMessage = QLabel('Welcome to the Home Physician!\nPlease Login!', parent = window)
userLabel = QLabel('User:', parent = window)
passLabel = QLabel('Pass:', parent = window)
userEntry = QLineEdit(window)
passEntry = QLineEdit(window)
loginButton = QPushButton('Login', parent = window)
newUserButton = QPushButton('Sign Up', parent = window)

#sign up page
enterName = QLabel("Full Name:", parent = signUpWindow)
enterHeight = QLabel("Height (cm):", parent = signUpWindow)
enterSex = QLabel("Sex:", parent = signUpWindow)
enterDOB = QLabel("DOB(YYYY-MM-DD)", parent = signUpWindow)
enterPin = QLabel("4 Digit Pin:", parent = signUpWindow)
createUser = QPushButton('Create User', parent = signUpWindow)
nameEntry = QLineEdit(signUpWindow)
heightEntry = QLineEdit(signUpWindow)
sexEntry = QLineEdit(signUpWindow)
dobEntry = QLineEdit(signUpWindow)
pinEntry = QLineEdit(signUpWindow)

createUser.clicked.connect(lambda:addNewUser())
createUser.clicked.connect(lambda:showUserCreated())

#placing the buttons on the sign up page
enterName.move(280,40)
enterHeight.move(280,110)
enterSex.move(280,180)
enterDOB.move(280,250)
enterPin.move(280,320)
nameEntry.move(410,40)
heightEntry.move(410,110)
sexEntry.move(410,180)
dobEntry.move(410,250)
pinEntry.move(410,320)
createUser.move(350,400)


#function to clear all widgets and get username and password, also opens the main page
def clearLoginScreen():
    testFunc()
    userName = userEntry.text()
    passWord = passEntry.text()
    passLabel.hide()
    userLabel.hide()
    welcomeMessage.hide()
    userEntry.hide()
    passEntry.hide()
    loginButton.hide()
    newUserButton.hide()
    print(userName + passWord)
    
   
def testFunc():
    print("pp nuts")
    
    global userName
    global passWord
    
    print(userName)
    print(passWord)
    
def clearMainPage():
    logoutButton.hide()
    PastDataButton.hide()
    pulseOximeterButton.hide()
    pupilDilationButton.hide() 
    bodyCameraButton.hide()
    weightButton.hide()
    bodyTempButton.hide()
    ailmentsAndPain.hide()
    bloodPressureButton.hide()
    showLoginPage()
    displayUser.hide()
    
def showLoginPage():
    passLabel.show()
    userLabel.show()
    welcomeMessage.show()
    userEntry.show()
    passEntry.show()
    loginButton.show()
    
def loginPage():
    #Welcome message 
    welcomeMessage.move(170, 15)
    welcomeMessage.setAlignment(QtCore.Qt.AlignCenter)

    #User and Pass Labels
    userLabel.setAlignment(QtCore.Qt.AlignCenter)
    userLabel.move(260, 180)
    
    passLabel.setAlignment(QtCore.Qt.AlignCenter)
    passLabel.move(260, 260)

    #user and pass entry widgets
    userEntry.move(400,180)
    userEntry.setStyleSheet("background-color: rgb(255,255,255)")
    
    passEntry.move(400,260)
    passEntry.setStyleSheet("background-color: rgb(255,255,255)")
    
    #Main header title font settings
    titleFont = QtGui.QFont()
    titleFont.setFamily("Linux Libertine O")
    titleFont.setPointSize(24)
    titleFont.setBold(True)
    titleFont.setItalic(True)
    titleFont.setWeight(75)

    #secondary header title font setting
    titleFont2 = QtGui.QFont()
    titleFont2.setFamily("Linux Libertine O")
    titleFont2.setPointSize(16)
    titleFont2.setBold(True)
    titleFont2.setItalic(True)
    titleFont2.setWeight(75)

    #setting the fonts to their labels
    welcomeMessage.setFont(titleFont)
    userLabel.setFont(titleFont2)
    passLabel.setFont(titleFont2)

    #creating the login push button
    loginButton.move(340,350)

    #when the button is pushed, clear the screen and open the GUI options for the main page, pass all the widgets
    #to the function as well
    #dont forget to get the username and password
    
    #will check if this user exists
    loginButton.clicked.connect(lambda:testFunc())
    loginButton.clicked.connect(lambda:userChecker())
     
    #loginButton.clicked.connect(lambda:clearLoginScreen())
    #loginButton.clicked.connect(lambda:showMainButtons())
    
    #sign up Button
    newUserButton.move(340,400)
    
    #when sign up button is clicked, it will open a new window that will allow the user to input their data: name, height, sex, dob
    newUserButton.clicked.connect(lambda:showSignUpPage())
    
#shows the sign up window
def showSignUpPage():
    signUpWindow.show()

#will take the user input and add the new user to the database
def addNewUser():
    global userName
    global newUserPin
    actualUserName = nameEntry.text()
    newUserPin = pinEntry.text()
    newUserHeight = heightEntry.text()
    newUserSex = sexEntry.text()
    newUserDOB = dobEntry.text()
    
    #make it so when the create new user button is pressed, it generates a userId and then adds the user ID and Pin to the database
    generateUserId(actualUserName)
    
    #add new user to USERS table first!!!!!!
    global addedUser
    
    addedUser = (userName,newUserPin)
    storeNewUser(conn,addedUser)
    
    #adding the new users info to the database
    global userProfileVariables
    userProfileVariables = (userName,actualUserName,newUserHeight,newUserSex,newUserDOB)
    storeUserInfo(conn,userProfileVariables)
    
def showUserCreated():
    global newUserPin
    global userName
    msg.show()
    msg.setIcon(QMessageBox.Information)
    msg.setText("User Successfully Created!\nYour Username will be: "+ userName + "\nYour password(pin entered) is: " + newUserPin)
    msg.setWindowTitle("User Created")
    msg.buttonClicked.connect(lambda:hidemsgBox())
    
def hidemsgBox():
    msg.hide()
    signUpWindow.hide()

#Used to make the widgets for the main page appear on-screen
def showMainButtons():
    logoutButton.setParent(window)
    logoutButton.show()
    
    PastDataButton.setParent(window)
    PastDataButton.show()
    
    pulseOximeterButton.setParent(window)
    pulseOximeterButton.show()
    
    pupilDilationButton.setParent(window)
    pupilDilationButton.show()
    
    bodyCameraButton.setParent(window)
    bodyCameraButton.show()
    
    weightButton.setParent(window)
    weightButton.show()
    
    bodyTempButton.setParent(window)
    bodyTempButton.show()
    
    ailmentsAndPain.setParent(window)
    ailmentsAndPain.show()
    
    bloodPressureButton.setParent(window)
    bloodPressureButton.show()
    
    #placement of all the main page buttons
    logoutButton.move(690,10)
    PastDataButton.move(10,430)
    
    bloodPressureButton.move(320,30)
    bloodPressureButton.resize(150,30)
    
    pulseOximeterButton.move(320,90)
    pulseOximeterButton.resize(150,30)
    
    pupilDilationButton.move(320,150)
    pupilDilationButton.resize(150,30)
    
    bodyCameraButton.move(320,210)
    bodyCameraButton.resize(150,30)
    
    weightButton.move(320, 270)
    weightButton.resize(150,30)
    
    bodyTempButton.move(320,330)
    bodyTempButton.resize(150,30)
    
    ailmentsAndPain.move(320,390)
    ailmentsAndPain.resize(150,30)
        
    #Staring with the logout function here
    logoutButton.clicked.connect(lambda:clearMainPage())
    
    #get user data to be displayed
    userData = getUserInfo()
    user_ID = userData[0]
    user_Name = userData[1]
    user_Height = userData[2]
    user_Sex = userData[3]
    user_Dob = userData[4]
    
    displayUser.show()
    displayUser.move(0,30)
    displayUser.setFrameStyle(0)
    displayUser.setPlainText("User ID: {}\nUser Name: {}\nHeight: {}\nSex: {}\nDOB: {}".format(user_ID,user_Name,user_Height,user_Sex,user_Dob))
    
#make main below this line
loginPage()


window.show()


    
    
    
    
    
    
    
    
    
    
    
    
    
sys.exit(app.exec_())
