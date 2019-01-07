#!/usr/bin/python

import sys
import json
from Tkinter import *
import Tkinter as tk
from firebase import firebase

firebase=firebase.FirebaseApplication('https://rpi-barcode.firebaseio.com/',None)



offline = False


global payload
with open("barcode.json") as f:
        payload = json.load(f)



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

def update_firebase(name, barcode, grade):
    data = {"Name":name, 'Grade':grade,'CheckIn':'0'}

    firebase.put('', 'Student/' + barcode, data)

def update_text(name, barcode, grade):
    data = {ss:{"Name":name, 'Grade':grade,'CheckIn':'0'}}

    payload.update(data)

    with open("barcode.json","w") as f:
        json.dump(payload, f)

def get_database():
    result = firebase.get('/Student',None)
    insert("end",result)
    return result


def find_text_in_text(barcode):

    name = payload[barcode]['Name']

    return name

def remove_from_text(barcode):

    name = payload[barcode]['Name']
            
    del payload[barcode]

    with open("barcode.json","w") as f:
        json.dump(payload, f)

    return name


def update_database():
    firebase.delete('',None)
    for key in payload:
        #print key
        data = {"Name":payload[key]['Name'], 'Grade':payload[key]['Grade'],'CheckIn':payload[key]['CheckIn']}
        sent = json.dumps(data)
        firebase.put('', 'Student/' + key, data)
    
def write_To_File():
    data = firebase.get('Student/',None)
    with open("barcode.json", "w") as outfile:
        json.dump(data, outfile)

def match_to_database():
    data = firebase.get('Student/',None)
    with open("barcode.json") as outfile:
        data_file = json.load(outfile)

    return ordered(data) == ordered(data_file)
    
def ordered(obj):
    if isinstance(obj,dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj,list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

class sample_app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(start_page)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class start_page(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Welcom to the main menu").pack(side = "top", fill = "x", pady = 10)

        global offline

        tk.Button(self, text = "Add a Student",command=lambda: master.switch_frame(add_student)).pack()

        tk.Button(self, text = "Remove a Student",command=lambda: master.switch_frame(remove_student)).pack()

        tk.Button(self, text = "Find Student",command=lambda: master.switch_frame(find_student)).pack()

        tk.Button(self, text = "Show students",command=lambda: master.switch_frame(show_all)).pack()

        tk.Button(self, text = "Check In",command=lambda: master.switch_frame(check_in)).pack()

            
        if not offline:

            tk.Button(self, text="Match Databse To File",command=lambda: master.switch_frame(matchFileToDB)).pack()

            tk.Button(self, text="Offline Mode",command=lambda: master.switch_frame(OfflineMode)).pack()
        else:

            tk.Button(self, text="Online Mode",command=lambda: master.switch_frame(OfflineMode)).pack()

        #endButton = Button(self,text="End Program",command=app.destroy).pack()

class add_student(tk.Frame):

    def __init__(self, master):
        global offline
        tk.Frame.__init__(self, master)
        self.master = master
        tk.Label(self, text = "Name").pack()
        self.entryBox = Entry(self)
        self.entryBox.pack(side = TOP, padx = 10, pady = 10)
        tk.Label(self, text = "Barcode").pack()
        self.entryBox1 = Entry(self)
        self.entryBox1.pack(side = TOP, padx = 10, pady = 10)
        tk.Label(self, text = "Students Level").pack()
        self.entryBox2 = Entry(self)
        self.entryBox2.pack(side = TOP, padx = 10, pady = 10)

        
        tk.Button(self, text = "Submit", width = 10, command = self.add).pack()
        tk.Button(self, text = "Return to main page", command = lambda: master.switch_frame(start_page)).pack()

    def add(self):
        popup = tk.Tk()
        name = self.entryBox.get().strip()
        label = tk.Label(popup, text=name+" added!")
        label.pack()
        barcode = self.entryBox1.get().strip()
        level = self.entryBox2.get().strip()
        self.entryBox.delete(0,'end')
        self.entryBox1.delete(0,'end')
        self.entryBox2.delete(0,'end')

        if not offline:
            update_firebase(name,barcode,level)
        else:
            update_text(name,barcode,level)
        end_button = Button(popup,text="OK",command=popup.destroy).pack()
        popup.mainloop()


class remove_student(tk.Frame):
    def __init__(self, master):
        global offline
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Barcode of Student you would like to remove").pack()
        self.entryBox = Entry(self)
        self.entryBox.pack(side = TOP, padx=10, pady=10)

        tk.Button(self, text="Submit",width =10,command=self.remove).pack()
        tk.Button(self, text="Return to start page",command=lambda: master.switch_frame(StartPage)).pack()

    def remove(self):
        popup = tk.Tk()

        barcode = self.entryBox.get().strip()
        if not offline:
            student_info = firebase.get(('/Student/'+barcode),'Name')

            self.entryBox.delete(0,'end')
            firebase.delete('/Student',barcode)


            label = tk.Label(popup, text=student_info+" removed!")
            label.pack()

        else:
            self.entryBox.delete(0,'end')
            label = tk.Label(popup, text=remove_from_text(barcode)+" removed!")
            label.pack()

        end_button = Button(popup,text="OK",command=popup.destroy).pack()
        popup.mainloop()

class find_student(tk.Frame):
    def __init__(self, master):
        global offline
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Scan the barcode of the student you would like to find").pack(side="top", fill="x", pady=10)

        self.entryBox = Entry(self)
        self.entryBox.pack(side = TOP, padx=10, pady=10)

        tk.Button(self, text="Submit",width =10,command=self.find).pack()
        tk.Button(self, text="Return to start page",command=lambda: master.switch_frame(start_page)).pack()

    def find(self):
        popup = tk.Tk()
        barcode = self.entryBox.get().strip()
        self.entryBox.delete(0,'end')

        if not offline:
            student_info = firebase.get(('/Student/'+barcode),'Name')
        else:
            student_info = find_student_in_text(barcode)
        if(student_info==None):
            student_info = "Student Not"
        label = tk.Label(popup, text = student_info + " found")
        label.pack()
        end_button = Button(popup,text="OK",command=popup.destroy).pack()
        popup.mainloop()


class show_all(tk.Frame):
    def __init__(self, master):
        global offline
        tk.Frame.__init__(self,master)
        tk.Label(self, text = "Show All").pack(side = "top", fill = "x",pady = 10)
        T = Text(self)
        T.pack()


        if not offline:
            data = firebase.get('',None)

            T.insert(END, "ID\t\t\tName\t\t\tGrade\t\t\tCheck in")
            for key in data['Student']:

                names= firebase.get('/Student/' + key,'Name')
                grades= firebase.get('/Student/' + key,'Grade')
                checks= firebase.get('/Student/' + key,'CheckIn')
            T.insert(END, key + '\t\t\t' + names + '\t\t\t' + grades + '\t\t\t' + checks + '\n')

        else:

            T.insert(END, "ID\t\t\tName\t\t\tGrade\t\t\tCheck in")

            
            for key in payload:
                y = payload[key]
                names= y["Name"]
                grades= y["Grade"]
                checks= y["CheckIn"]
                T.insert(END, key + '\t\t\t' + names + '\t\t\t' + grades + '\t\t\t' + checks + '\n')



        tk.Button(self, text= "Return to main page", command=lambda: master.switch_frame(start_page)).pack()

class check_in(tk.Frame):
    def __init__(self, master):
        global offline
        tk.Frame.__init__(self, master)
        tk.Label(self, text= "Scan the barcode of the student you would like to Check In").pack(side = "top", fill = "x", pady = 10)

        self.entryBox = Entry(self)
        self.entryBox.pack(side = TOP, padx = 10 , pady = 10)

        tk.Button(self, text= "Submit", width =10, command=self.find).pack()
        tk.Button(self, text= "Return to start page", command=lambda: master.switch_frame(start_page)).pack()

    def find(self):
        popup = tk.Tk()
        barcode = self.entryBox.get().strip()
        self.entryBox.delete(0, 'end')

        if not offline:
            student_info = firebase.get(('/Student/' + barcode), 'Name')
            if(student_info==None):
                student_info = "Student Not"
            else:
                check= firebase.get('/Student/' + barcode, 'CheckIn')
                name= firebase.get('/Student/' + barcode, 'Name')
                grade= firebase.get('/Student/' + barcode, 'Grade')
                num_checks=int(check)
                num_checks=num_checks+1
                data = {"Name":name, 'Grade':grade,'CheckIn':str(num_checks)}
                firebase.put('', 'Student/' + barcode, data)

        else:
            student_info = None
            for key in payload:
                if barcode == key:
                    check = int(payload[key]['CheckIn'])
                    payload[key]['CheckIn'] = str(check+1)
                    student_info = payload[key]['Name']
            
        label = tk.Label(popup, text = student_info + " found")
        label.pack()
        end_button = Button(popup, text= "OK", command= popup.destroy).pack()
        popup.mainloop()


class offline_mode(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global offline
        if offline:
            tk.Label(self, text= "Offline Mode is now Active").pack(side = "top", fill = "x", pady = 10)
            offline = False
        else:
            tk.Label(self, text= "Offline Mode is now Deacticated").pack(side = "top", fill = "x", pady = 10)
            offline = True

        tk.Button(self, text = "Return to start page", command=lambda: master.switch_frame(start_page)).pack()



class get_database(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        write_To_file()
        tk.Label(self, text= "File Updated").pack(side="top", fill="x", pady=10)
        tk.Button(self, text= "Return to start page", command=lambda: master.switch_frame(start_page)).pack()
        


class write_to_database(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        update_database()
        tk.Label(self, text = "DataBase Updated!").pack(side = "top", fill = "x", pady = 10)
        tk.Button(self, text = "Return to start page", command = lambda: master.switch_frame(start_page)).pack()

        

class match_file_to_database(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        match = match_to_database()
        if match:
            tk.Label(self, text = "Matched").pack(side = "top", fill = "x", pady = 10)
        else:
            tk.Label(self, text = "Did not Matched").pack(side = "top", fill = "x", pady = 10)
            tk.Button(self, text = "OverWrite Database", command=lambda: master.switch_frame(write_to_database)).pack()
            tk.Button(self, text = "OverWrite Json File", command=lambda: master.switch_frame(get_database)).pack()
            
        tk.Button(self, text = "Return to start page", command=lambda: master.switch_frame(start_page)).pack()

if __name__ == "__main__":
    app = sample_app()
    char = ''
    app.title("Barcode Reader")
    app.mainloop()
