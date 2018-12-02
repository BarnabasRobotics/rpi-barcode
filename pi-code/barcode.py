#!/usr/bin/python

import sys
import json
from Tkinter import *
import Tkinter as tk
from firebase import firebase

firebase = firebase.FirebaseApplication("https://rpi-barcode.firebaseio.com/", None)

def barcode_reader():
    """Barcode code obtained from 'brechmos' 
    https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
    
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',

           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',

           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',

           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}
    
    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',

            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',

            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',

            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open('/dev/hidraw0', 'rb')
    ss = ""
    shift = False
    done = False
    
    while not done:
        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if ord(c) > 0:
                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(ord(c)) == 40:
                    done = True
                    break
                
                ##  If we are shifted then we have to
                ##  use the hid2 characters.
                
                if shift:
                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[int(ord(c))]
                        shift = False
            
                ##  If we are not shifted then use
                ##  the hid characters
                else:
                    ## If it is a '2' then it is the shift key
                    if int(ord(c)) == 2:
                        shift = True
                
                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid[int(ord(c))]
                        
    return ss

def update_firebase(name, ss, grade):
    data = {"Name" : name, 'Grade' : grade}
    sent = json.dumps(data)
    firebase.put('', 'Student/' + ss, data)

def add_Student(root):
    print("Enter student's name: ")
    name = raw_input()

    print("Enter student's Grade: ")
    grade = raw_input()

    print("Please scan barcode: ")
    ss = barcode_reader()

    buff = raw_input()
    update_firebase(name,ss,grade)

def get_DataBase():
    result = firebase.get('/Student', None)

    insert("end", result)
    return result

def remove_Student():
    print("Please scan barcode of student you would like to remove: ")
    
    ss = barcode_reader()
    buff = raw_input()
    
    firebase.delete('/Student',ss)
    print 'Removed'

def update_Student():
    # Could update one value or create a new user with same code, 
    # possible to use create_Student instead
    print("Please scan barcode of student you would like to Update: ")

    ss = barcode_reader()
    buff = raw_input()

    print 'Updated'
    
def find_Student():
    print("Please scan barcode: ")
    ss = barcode_reader()
    buff = raw_input()

    print ''

    studentInfo = firebase.get(('/Student/' + ss), None)
    print studentInfo

def parse_Json():
    """TODO: Find a better way to parse it"""
    
    data = firebase.get('', None)
    parsed_json = json.loads(data)

    # print(parsed_json['Name'])
    
    for key in data['Student']:
        print key

def write_To_File():
    data = firebase.get('', None)
    for key in data['Student']:
        file.write(key+',')

    print 'File Updated'

def printToGUI():
    with open("barcodes.text", "r")as f:
        Label(root, text = f.read()).pack()

class SampleApp(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcom to the main menu").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Add a Student",command=lambda: master.switch_frame(AddStudent)).pack()
        
        tk.Button(self, text="Remove a Student",command=lambda: master.switch_frame(RemoveStudent)).pack()

        tk.Button(self, text="Find Student",command=lambda: master.switch_frame(FindStudent)).pack()

        tk.Button(self, text="Offline Mode",command=lambda: master.switch_frame(OfflineMode)).pack()

        getButton = Button(self,text="Get Database",command=get_DataBase)
        #getButton.pack()
        
        updateButton = Button(self,text="Update Student",command=update_Student)
        #updateButton.pack()
        
        showButton = Button(self,text="Show students",command=printToGUI)
        #showButton.pack()

        writeButton = Button(self,text="Write To File",command=write_To_File)
        #writeButton.pack()

        #endButton = Button(self,text="End Program",command=app.destroy).pack()

class AddStudent(tk.Frame):

    def __init__(self, master):
        
        tk.Frame.__init__(self, master)
        self.master = master
        
        tk.Label(self, text="Name").pack()
        self.entryBox = Entry(self)
        self.entryBox.pack(side = TOP, padx=10, pady=10)
        tk.Label(self,text="Barcode").pack()
        self.entryBox1 = Entry(self)
        self.entryBox1.pack(side = TOP, padx=10, pady=10)
        tk.Label(self,text="Students Level").pack()
        self.entryBox2 = Entry(self)
        self.entryBox2.pack(side = TOP, padx=10, pady=10)

        tk.Button(self, text="Submit",width =10,command=self.add).pack()
        tk.Button(self, text="Return to main page",command=lambda: master.switch_frame(StartPage)).pack()

    def add(self):
        popup = tk.Tk()
        name = self.entryBox.get().strip()
        label = tk.Label(popup, text=name+" added!")
        label.pack()
        #print name
        barcode = self.entryBox1.get().strip()
        #print barcode
        level = self.entryBox2.get().strip()
        #print level
        self.entryBox.delete(0,'end')
        self.entryBox1.delete(0,'end')
        self.entryBox2.delete(0,'end')
        
        update_firebase(name,barcode,level)
        endButton = Button(popup,text="OK",command=popup.destroy).pack()
        popup.mainloop()


class RemoveStudent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Barcdoe of Student you would like to remove").pack()
        self.entryBox = Entry(self)
        self.entryBox.pack(side = TOP, padx=10, pady=10)
        
        tk.Button(self, text="Submit",width =10,command=self.remove).pack()
        tk.Button(self, text="Return to start page",command=lambda: master.switch_frame(StartPage)).pack()

    def remove(self):
        popup = tk.Tk()

        barcode = self.entryBox.get().strip()
        #print barcode

        studentInfo = firebase.get(('/Student/'+barcode),'Name')

        self.entryBox.delete(0,'end')
        firebase.delete('/Student',barcode)

        
        label = tk.Label(popup, text=studentInfo+" removed!")
        label.pack()

        endButton = Button(popup,text="OK",command=popup.destroy).pack()
        popup.mainloop()

class FindStudent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Scan the barcode of the student you would like to find").pack(side="top", fill="x", pady=10)

        self.entryBox = Entry(self)
        self.entryBox.pack(side = TOP, padx=10, pady=10)

        tk.Button(self, text="Submit",width =10,command=self.find).pack()
        tk.Button(self, text="Return to start page",command=lambda: master.switch_frame(StartPage)).pack()

    def find(self):
        popup = tk.Tk()
        label = tk.Label(popup, text="Person found!")
        label.pack()
        barcode = self.entryBox.get().strip()
        #print barcode
        self.entryBox.delete(0,'end')
        studentInfo = firebase.get(('/Student/'+barcode),None)
        print studentInfo
        endButton = Button(popup,text="OK",command=popup.destroy).pack()
        popup.mainloop()

class OfflineMode(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        tk.Label(self, text = "Welcome to Offline Mode").pack(side = "top", fill = "x", pady = 10)

        ##take input and update database
        tk.Button(self, text = "Return to start page", command = lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":

    app = SampleApp()

    file = open("barcodes.text", "a")
    char = ''
    app.title("Barcode Reader")
    file.close()

    app.mainloop()
