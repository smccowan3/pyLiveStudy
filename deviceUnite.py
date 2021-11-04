import sys
import subprocess
import live
import time
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

##global variables##

currentSet = 0
copyPermission = False
origSet = live.Set()
origVals = []
destSet = live.Set()
trackName = None
deviceName = None
trackTarget = None
deviceTarget = None

##window class##

def window():
   app = QApplication(sys.argv)
   widget = QWidget()
   
   button1 = QPushButton(widget)
   button1.setText("Open Origin        ")
   button1.move(0,32)
   button1.clicked.connect(button1_clicked)
   

   button2 = QPushButton(widget)
   button2.setText("Open Destination")
   button2.move(0,64)
   button2.clicked.connect(button2_clicked)

   button3 =QPushButton(widget)
   button3.setText("Copy Contents")
   button3.move(150,32)
   button3.clicked.connect(button3_clicked)


   button4 =QPushButton(widget)
   button4.setText("Place Contents")
   button4.move(150,64)
   button4.clicked.connect(button4_clicked)


   button5 =QPushButton(widget)
   button5.setText("Track Name  ")
   button5.move(300,32)
   button5.clicked.connect(button5_clicked)

   button6 =QPushButton(widget)
   button6.setText("Device Name")
   button6.move(300,64)
   button6.clicked.connect(button6_clicked)


   widget.setGeometry(200,200,700,100)
   widget.setWindowTitle("Basic EQ Alignment App")
   widget.show()
   sys.exit(app.exec_())


##checking information methods##
def trackInObjectArr(array, value):
    global trackTarget
    present = False
    for i in range(len(array)):
        if array[i].name == value:
            present = True
            trackTarget = i
    return present

def deviceInObjectArr(array, value):
     global deviceTarget
     present = False
     for i in range(len(array)):
        if array[i].name == value:
            present = True
            deviceTarget = i
     return present

    
    

#open origin file#
def button1_clicked():
   global currentSet
   print("Opening File One")
   originPath = QFileDialog.getOpenFileName(None, 'Open a file', '','All Files (*.*)')
   currentSet = 1
   print("Origin Path is " + originPath[0])
   subprocess.call(['open', originPath[0]])

#open destination file#
def button2_clicked():
   global currentSet
   print("Opening File Two")
   destPath = QFileDialog.getOpenFileName(None, 'Open a file', '','All Files (*.*)')
   currentSet = 2
   print("Destination Path is " + destPath[0])
   subprocess.call(['open', destPath[0]])
   
#copy contents of orig file#
def button3_clicked():
   global origSet, trackName, deviceName, trackTarget, deviceTarget, copyPermission, origVals
   origVals = []
   print("Now verifying track names and device names in set. Please wait a moment")
   origSet.scan(scan_devices = True)
   # first check track and device name present
   if trackName == "":
       print("Please enter a track name first")
   elif deviceName == "":
       print("Please enter a device name first")
   elif not(trackInObjectArr(origSet.tracks, trackName)):
       print("No valid track target " + trackName + " in Live Set")
   elif not(deviceInObjectArr(origSet.tracks[trackTarget].devices, deviceName)):
       print("No valid device target " + deviceName + " in Live Set")
   else:
       print("First scanning contents for track named " + trackName)
       print(origSet.tracks[trackTarget].name +  " has " + origSet.tracks[trackTarget].devices[deviceTarget].name + " device with " + str(len(origSet.tracks[0].devices[0].parameters)) + " parameters")
       print("Now copying please wait...")
       for i in range(len(origSet.tracks[trackTarget].devices[deviceTarget].parameters)):
          origVals.append(origSet.tracks[trackTarget].devices[deviceTarget].parameters[i].value[3])
       print("Content copied successfully. Please now open a destination file from the main menu.")
       copyPermission = True
    
#paste contents from orig file to dest file# 
def button4_clicked():
   global currentSet, origSet, destSet, trackName, deviceName, trackTarget, deviceTarget, copyPermission, origVals
   if not(copyPermission):
       print("Content is not copied. Please enter track name, device name and copy contents of the origin file")
   elif currentSet != 2:
       print("Current opened set is not a destination. You cannot copy a file's parameters to itself")
   else:
       destSet.scan(scan_devices = True)
       # perform checks #
       if trackName == "":
           print("Please enter a track name first")
       elif deviceName == "":
           print("Please enter a device name first")
       elif not(trackInObjectArr(destSet.tracks, trackName)):
           print("No valid track target " + trackName + " in Live Set")
       elif not(deviceInObjectArr(destSet.tracks[trackTarget].devices, deviceName)):
           print("No valid device target " + deviceName + " in Live Set")
       else:
           #print("orig set is at " + str(origSet.tracks[trackTarget].devices[deviceTarget].name))
           #print("dest set is at " + str(destSet.tracks[trackTarget].devices[deviceTarget].name))
           print("Placing Contents")
           for i in range (len(destSet.tracks[trackTarget].devices[deviceTarget].parameters)):
                 print("setting parameter " + str(i))
                 print("origin parameter is " + str(origVals[i]))
                 print("destination parameter is " + str(destSet.tracks[trackTarget].devices[deviceTarget].parameters[i].value[3]))
                 destSet.tracks[trackTarget].devices[deviceTarget].parameters[i].value = origVals[i]
                 print("destination parameter is now " + str(destSet.tracks[trackTarget].devices[deviceTarget].parameters[i].value[3]))
                 print("parameter " + str(i+1) + " is set.")
                       
           print("Parameters set successfully")
       

#set track name#
def button5_clicked():
   global trackName
   print("Setting track name")
   trackName, ok = QInputDialog.getText(None, "TRACK ENTRY", "Enter the origin and target track name \nFor example: Piano")
   print("Track name is " + trackName)
   
#set device name#
def button6_clicked():
   global deviceName
   print("Setting device name")
   deviceName, ok = QInputDialog.getText(None, "DEVICE ENTRY", "Enter the origin and target device name \nFor example: EQ Eight")
   print("Device name is " + deviceName)
   
if __name__ == '__main__':
   window()
