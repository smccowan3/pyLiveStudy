import sys
import subprocess
import live
import time
import os
from functools import partial
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

##global variables##
trackName = "Kick"
deviceName = "EQ Eight"
mySet = live.Set()
EQList = [[None]*10, [None]*10, [None]*10, [None]*10]


##method to find kick/eq location##
def inObjectArr(array, value):
    location = None
    for i in range(len(array)):
        if array[i].name == value:
            location = i
    return location


##window class##

def window():
    app = QApplication(sys.argv)
    widget = QWidget()

    button1 = QPushButton(widget)
    button1.setText("Open Ableton File")
    button1.move(0, 32)
    button1.clicked.connect(button1_clicked)

    button2 = QPushButton(widget)
    button2.setText("Track Name")
    button2.move(0, 64)
    button2.clicked.connect(button2_clicked)

    button3 = QPushButton(widget)
    button3.setText("EQ 1 Set")
    button3.move(150, 32)
    button3.clicked.connect(partial(setEQ, 0))

    button4 = QPushButton(widget)
    button4.setText("EQ 1 Place")
    button4.move(150, 64)
    button4.clicked.connect(partial(placeEQ, 0))

    button5 = QPushButton(widget)
    button5.setText("EQ 2 Set")
    button5.move(300, 32)
    button5.clicked.connect(partial(setEQ, 1))

    button6 = QPushButton(widget)
    button6.setText("EQ 2 Place")
    button6.move(300, 64)
    button6.clicked.connect(partial(placeEQ, 1))

    button7 = QPushButton(widget)
    button7.setText("EQ 3 Set")
    button7.move(450, 32)
    button7.clicked.connect(partial(setEQ, 2))

    button8 = QPushButton(widget)
    button8.setText("EQ 3 Place")
    button8.move(450, 64)
    button8.clicked.connect(partial(placeEQ, 2))

    button9 = QPushButton(widget)
    button9.setText("EQ 4 Place")
    button9.move(600, 32)
    button9.clicked.connect(partial(setEQ, 3))

    button10 = QPushButton(widget)
    button10.setText("EQ 4 Set")
    button10.move(600, 64)
    button10.clicked.connect(partial(placeEQ, 3))

    button11 = QPushButton(widget)
    button11.setText("Dump and Scan")
    button11.move(750, 48)
    button11.clicked.connect(button11_clicked)

    widget.setGeometry(200, 200, 1000, 100)
    widget.setWindowTitle("Kick Mixing App")
    widget.show()
    sys.exit(app.exec_())


def button1_clicked():
    global mySet
    print("button 1 has been clicked")
    print("Opening File One")
    originPath = QFileDialog.getOpenFileName(None, 'Open a file', '', 'Als (*.als)')
    print("Origin Path is " + originPath[0])
    subprocess.call(['open', originPath[0]])
    mySet.scan(scan_devices=True)


def button2_clicked():
    print("button 2 has been clicked")
    global trackName
    print("Setting track name")
    trackName, ok = QInputDialog.getText(None, "TRACK ENTRY",
                                         "Enter the origin and target track name \nFor example: Piano")
    print("Track name is " + trackName)


def setEQ(lox):
    global mySet, trackName
    print("setting EQ parameter " + str(lox))
    mySet.scan(scan_devices=True)
    index = inObjectArr(mySet.tracks, trackName)
    startLoc = 4+10*lox
    counter = 0
    for i in range(startLoc, startLoc+10):
        EQList[lox][counter] = mySet.tracks[index].devices[1].parameters[i].value[3]
        counter += 1
    print("eq recorded")

def placeEQ(lox):
    global mySet, trackName
    print("placing EQ parameter " + str(lox))
    mySet.scan(scan_devices=True)
    index = inObjectArr(mySet.tracks, trackName)
    startLoc = 4 + 10 * lox
    counter = 0
    for i in range(startLoc, startLoc + 10):
        mySet.tracks[index].devices[1].parameters[i].value = EQList[lox][counter]
        counter += 1
    print("eq placed")


# set device name#
def button11_clicked():
    global mySet, trackName
    print("now dumping")
    mySet.scan(scan_devices=True)
    #mySet.dump()
    index = inObjectArr(mySet.tracks, trackName)
    for i in range((len(mySet.tracks[index].devices[1].parameters))):
        print(mySet.tracks[index].devices[1].parameters[i].value)


if __name__ == '__main__':
   window()

