# +++++++++++++MODULE++++++++++++++++
from cgitb import text
from logging import root
from sre_parse import State
from tkinter import *
from tkcalendar import Calendar
from tkinter import messagebox
import pickle
import time
from datetime import date, datetime
from random import randint
import os.path
from tkinter import filedialog
import shutil 
from PIL import Image, ImageTk
import qrcode 
from time import *
import pymongo



#+++++++++++++++DATABASE+++++++
#myclient = pymongo.MongoClient("mongodb+srv://bishalde:5741@cluster0.d3qd0.mongodb.net/studentmanagement?retryWrites=true&w=majority")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["StudentManagement"]
mycol = mydb["StudentData"]


# ++++++++++++++++WINDOW++++++++++++++++
window = Tk()
window.title("Login")
window.geometry("650x750")
logo = PhotoImage(file="Resources/logow.png")
window.iconphoto(False, logo)
# window.geometry("1535x863") ------ my pc resolutuion

'''To get your Monitor's width'''
#screen_width = window.winfo_screenwidth()

'''To get your Monitor's height'''
#screen_height = window.winfo_screenheight()

'''Inserting values'''
# size=str(screen_width)+'x'+str(screen_height)
# window.geometry(size)

'''Make window Non-Resizable'''
window.resizable(0, 0)

''' Remove maximize,minimize,cancel buttons'''
# window.overrideredirect(True)


def addstudent():
    addstd = Toplevel()
    addstd.geometry('%dx%d+%d+%d' % (1400, 800, 100, 10))
    addstd.resizable(0, 0)

    def UploadAction():
        filename = filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png")),parent=addstd)

        destination ="images/"
        dest = shutil.copy(filename, destination) 

        image1 = Image.open(dest)
        resize_img = image1.resize((150, 200))
        test = ImageTk.PhotoImage(resize_img)

        label1 = Label(addstd,image=test)
        label1.image = test
        label1.place(x=1125, y=90)
        name=filename.split('/')
        le=len(name)
        label2.config(text=name[le-1])
        photobutton.config(text="change",bg="brown",fg='white')

    def qrgen(studentname,dob,gender,image):
        with open("count.txt", "r") as f:
            a=int(f.read())

        s="Student name :- {} \nStudent DOB :- {} \nStudent Gender :- {} \nImage Location :- {} ".format(studentname,dob,gender,image)
        print(s) 

        obj_qr = qrcode.QRCode(version = 5,error_correction = qrcode.constants.ERROR_CORRECT_L,box_size = 3,)  
        obj_qr.add_data(s)  
        obj_qr.make(fit = True)
        qr_img = obj_qr.make_image(fill_color = "blue", back_color = "white")  
        draft = "QRcodes/"+studentname+'.png'
        qr_img.save(draft)   

        image1 = Image.open(draft)
        resize_img = image1.resize((200, 230))
        test = ImageTk.PhotoImage(resize_img)
        label2 = Label(addstd,image=test)
        label2.image = test
        label2.place(x=1100, y=300)
        generateqr.config(text="GENERATED",bg='brown',fg="white",state="disabled")

        mydict = { "_id":a,"Student_name":studentname,"DOB":dob,"Gender": gender,"Image_location":image}
        x=mycol.insert_one(mydict)
        if(x.inserted_id==a):
            with open("count.txt", "w") as f:
                a=a+1
                f.write(str(a))

            messagebox.showinfo("Done","record Inserted",parent=addstd)
        

    
    randomnumber = str(randint(1, 4))
    bbgimage = PhotoImage(file="Resources/bg"+randomnumber+".png")
    bbg = Label(addstd, image=bbgimage)
    bbg.pack()

    box = LabelFrame(addstd, height="720", width="1300", bg='white', bd=0)
    box.place(x=45, y=40)

    a1 = Frame(addstd, height=700, width=590, bg="white")
    a1.place(x=50, y=50)

    introlabel = Label(addstd,text="Add New Student Detail Here", font=("Berlin Sans FB", 23, "bold"), bg='white', fg='blue')
    introlabel.place(x=55, y=55)

    # studentname section ------------------------------------------
    studentnamelable = Label(addstd, text="Student Name :", font=("Bahnschrift", 12, "bold"), bg='white')
    studentnamelable.place(x=55, y=110)

    studentname = Entry(addstd, width=30,bg="yellow", font=("Arial",12), fg="blue")
    studentname.place(x=55, y=140)

    studentDOBlable = Label(addstd, text="Student DOB :", font=("Bahnschrift", 12, "bold"), bg='white')
    studentDOBlable.place(x=380, y=110)

    dob = Entry(addstd, width=20,bg="yellow", font=("Arial",12), fg="blue")
    dob.place(x=385, y=140)

    #gender lable ---------------------------
    genderlable = Label(addstd, text="Gender :", font=("Bahnschrift", 12, "bold"), bg='white')
    genderlable.place(x=600, y=110)

    #genderentery-----------------------
    clicker=StringVar()
    clicker.set("Select Gender")
    gender=OptionMenu(addstd,clicker,"Male","Female","Other")
    gender.place(x=600,y=135)
    gender.config(fg="blue")
    gender["menu"].config(bg="white")
    gender["menu"].config(fg="blue")

    #photo lable ---------------------------
    photolable = Label(addstd, text="Picture :", font=("Bahnschrift", 12, "bold"), bg='white')
    photolable.place(x=750, y=110)

    photobutton=Button(addstd, text='Add Image',cursor="hand2",command=UploadAction)
    photobutton.place(x=750,y=140)

    label2 = Label(addstd,text="No File Selected", font=("Bahnschrift", 10,"bold"), bg='white',fg="blue")
    label2.place(x=820, y=145)

    studentmobilenumberlable = Label(addstd, text="Student Mobile Number :", font=("Bahnschrift", 12, "bold"), bg='white')
    studentmobilenumberlable.place(x=55, y=165)

    stuentmobilenumber = Entry(addstd, width=20,bg="yellow", font=("Arial",12), fg="blue")
    stuentmobilenumber.place(x=55, y=195)

    stuentemaillable = Label(addstd, text="Student E-mail :", font=("Bahnschrift", 12, "bold"), bg='white')
    stuentemaillable.place(x=280, y=165)

    studentemail = Entry(addstd, width=25,bg="yellow", font=("Arial",12), fg="blue")
    studentemail.place(x=600, y=195)

    stuentaadharlable = Label(addstd, text="Student Aadhar Number :", font=("Bahnschrift", 12, "bold"), bg='white')
    stuentaadharlable.place(x=600, y=165)

    studentaadhar = Entry(addstd, width=30,bg="yellow", font=("Arial",12), fg="blue")
    studentaadhar.place(x=285, y=195)

    # fathersname section ------------------------------------------
    fathernamelable = Label(addstd, text="Father Name :", font=("Bahnschrift", 12, "bold"), bg='white')
    fathernamelable.place(x=55, y=168+75)

    fathername = Entry(addstd, width=30,bg="yellow", font=("Arial",12), fg="blue")
    fathername.place(x=55, y=195+75)

    FATHERDOBlable = Label(addstd, text="Father DOB :", font=("Bahnschrift", 12, "bold"), bg='white')
    FATHERDOBlable.place(x=380, y=168+75)

    fatherdob = Entry(addstd, width=20,bg="yellow", font=("Arial",12), fg="blue")
    fatherdob.place(x=385, y=195+75)
    
    FATHERqualificationlable = Label(addstd, text="Father Qualification :", font=("Bahnschrift", 12, "bold"), bg='white')
    FATHERqualificationlable.place(x=600, y=168+75)

    fatherqualification = Entry(addstd, width=18,bg="yellow", font=("Arial",12), fg="blue")
    fatherqualification.place(x=600, y=195+75)

    FATHERoccupationlable = Label(addstd, text="Father Occupation :", font=("Bahnschrift", 12, "bold"), bg='white')
    FATHERoccupationlable.place(x=795, y=168+75)

    fatheroccupation = Entry(addstd, width=18,bg="yellow", font=("Arial",12), fg="blue")
    fatheroccupation.place(x=800, y=195+75)

    fathermobilenumberlable = Label(addstd, text="Father Mobile Number :", font=("Bahnschrift", 12, "bold"), bg='white')
    fathermobilenumberlable.place(x=55, y=225+75)

    fathermobilenumber = Entry(addstd, width=20,bg="yellow", font=("Arial",12), fg="blue")
    fathermobilenumber.place(x=55, y=255+75)

    FATHERemaillable = Label(addstd, text="Father E-mail :", font=("Bahnschrift", 12, "bold"), bg='white')
    FATHERemaillable.place(x=280, y=225+75)

    fatheremail = Entry(addstd, width=25,bg="yellow", font=("Arial",12), fg="blue")
    fatheremail.place(x=285, y=255+75)


    # Mothername section ------------------------------------------
    mothernamelable = Label(addstd, text="Mother Name :", font=("Bahnschrift", 12, "bold"), bg='white')
    mothernamelable.place(x=55, y=400)

    mothername = Entry(addstd, width=30,bg="yellow", font=("Arial",12), fg="blue")
    mothername.place(x=55, y=430)

    motherDOBlable = Label(addstd, text="Mother DOB :", font=("Bahnschrift", 12, "bold"), bg='white')
    motherDOBlable.place(x=380, y=400)

    motherdob = Entry(addstd, width=20,bg="yellow", font=("Arial",12), fg="blue")
    motherdob.place(x=385, y=430)
    
    motherqualificationlable = Label(addstd, text="Mother Qualification :", font=("Bahnschrift", 12, "bold"), bg='white')
    motherqualificationlable.place(x=600, y=400)

    motherqualification = Entry(addstd, width=18,bg="yellow", font=("Arial",12), fg="blue")
    motherqualification.place(x=600, y=430)

    motheroccupationlable = Label(addstd, text="Mother Occupation :", font=("Bahnschrift", 12, "bold"), bg='white')
    motheroccupationlable.place(x=795, y=400)

    motheroccupation = Entry(addstd, width=18,bg="yellow", font=("Arial",12), fg="blue")
    motheroccupation.place(x=800, y=430)

    mothermobilenumberlable = Label(addstd, text="Mother Mobile Number :", font=("Bahnschrift", 12, "bold"), bg='white')
    mothermobilenumberlable.place(x=55, y=460)

    mothermobilenumber = Entry(addstd, width=20,bg="yellow", font=("Arial",12), fg="blue")
    mothermobilenumber.place(x=55, y=490)

    FATHERemaillable = Label(addstd, text="Father E-mail :", font=("Bahnschrift", 12, "bold"), bg='white')
    FATHERemaillable.place(x=280, y=460)

    fatheremail = Entry(addstd, width=25,bg="yellow", font=("Arial",12), fg="blue")
    fatheremail.place(x=285, y=490)



    generateqr= Button(addstd, text="QR generate", font=("Candara", 10, "bold"), bg='Blue', fg='white', command=lambda : qrgen(studentname.get(),dob.get(),clicker.get(),label2['text']))
    generateqr.place(x=400, y=600)










    '''# studentname section ------------------------------------------
    studentnamelable = Label(addstd, text="Student Name :", font=(
        "Bahnschrift", 15, "bold"), bg='white')
    studentnamelable.place(x=55, y=110)
    studentname = Entry(addstd, width=30,
                        bg="yellow", font=(8), fg="blue")
    studentname.place(x=250, y=117)

    # class & section sector------------------------------------------
    classslable = Label(addstd, text="Class :", font=(
        "Bahnschrift", 15, "bold"), bg='white')
    classslable.place(x=55, y=150)
    classs = Entry(addstd, width=10,
                   bg="yellow", font=(8), fg="blue")
    classs.place(x=250, y=157)

    sectionlable = Label(addstd, text="Section :", font=(
        "Bahnschrift", 15, "bold"), bg='white')
    sectionlable.place(x=365, y=151)
    section = Entry(addstd, width=8,
                    bg="yellow", font=(8), fg="blue")
    section.place(x=450, y=157)

    # father's name section ---------------------------------------------------------
    fathernamelable = Label(addstd, text="Father's Name :", font=(
        "Bahnschrift", 15, "bold"), bg='white')
    fathernamelable.place(x=55, y=190)
    fathername = Entry(addstd, width=30,
                       bg="yellow", font=(8), fg="blue")
    fathername.place(x=250, y=197)

    # mother's name section-----------------------------------------------------------
    mothernamelable = Label(addstd, text="Mothers's Name :", font=(
        "Bahnschrift", 15, "bold"), bg='white')
    mothernamelable.place(x=55, y=230)
    mothername = Entry(addstd, width=30,
                       bg="yellow", font=(8), fg="blue")
    mothername.place(x=250, y=237)

    # date of birth section-----------------------------------------------------------
    doblable = Label(addstd, text="Date Of Birth :",
                     font=("Bahnschrift", 15, "bold"), bg='white')
    doblable.place(x=55, y=270)
    dob = Entry(addstd, width=30, bg="yellow", font=(8), fg="blue")
    dob.place(x=250, y=277)

    # admission number section-----------------------------------------------------------
    admissionnumberlable = Label(addstd, text="Admission Number :", font=(
        "Bahnschrift", 15, "bold"), bg='white')
    admissionnumberlable.place(x=55, y=310)
    admissionnumber = Entry(addstd, width=30,
                            bg="yellow", font=(8), fg="blue")
    admissionnumber.place(x=250, y=317)

    # address section---------------------------------------------------------------------
    addressable = Label(addstd, text="Address :", font=(
        "Bahnschrift", 15, "bold"), bg='white')
    addressable.place(x=55, y=350)
    address = Entry(addstd, width=30,
                    bg="yellow", font=(8), fg="blue")
    address.place(x=250, y=357)

    # buttons section-------------------------------------------------------------------------
    addbutton = Button(addstd, text="ADD", cursor="hand2", bd=3)
    addbutton.place(x=200, y=475)

    resetbutton = Button(addstd, text="RESET",cursor="hand2", bd=3)
    resetbutton.place(x=365, y=472)
'''
    addstd.mainloop()


def login(usernamee, passwordd):
    if os.path.isfile("password.dat"):
        if len(usernamee) != 0:
            if len(passwordd) != 0:
                F = open('password.dat', 'ab')
                F.close()
                with open('password.dat', 'rb') as Myfile:
                    c = 0
                    l = 0
                    while True:
                        try:
                            a = pickle.load(Myfile)
                            if a[0] == usernamee and a[1] == passwordd:
                                l = l+1

                                #messagebox.showinfo("Login","Login Successfull.!")
                                username.delete(0, END)
                                password.delete(0, END)
                                reset()
                            else:
                                c = c+1
                                l = l+1

                        except EOFError:
                            break

                if c == l:
                    intro = "Username And Password Did Not Matched"
                    messagebox.showerror("Login", intro)

            else:
                messagebox.showwarning("WARNING", "Please Enter Password.!")

        else:
            messagebox.showwarning("WARNING", "Please Enter UserName.!")
    else:
        messagebox.showinfo(
            "NO PRE-EXISTING DATA", "No Pre-exesting username And Password Found!.\n\nCreate New profile")


def reset():
    loginframe.destroy()
    loginlabel.destroy()
    username.destroy()
    usernamelable.destroy()
    password.destroy()
    passwordlable.destroy()
    vvv.destroy()
    vv.destroy()
    loginbutton.destroy()
    into.destroy()

    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    w = w-10
    h = h-10
    x = 0
    y = 0
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    window.resizable(True, True)

    mainframe = LabelFrame(bg, text="", bg="white", width=1400, height=740)
    mainframe.place(x=60, y=50)

    addbtn = Button(window, text="New Student", font=(
        "Candara", 10, "bold"), bg='Blue', fg='white', command=addstudent)
    addbtn.place(x=80, y=80)


randomnumber = str(randint(1, 4))
bgimage = PhotoImage(file="Resources/bg"+randomnumber+".png")
loginicon = PhotoImage(file="Resources/loginicon.png")
passicon = PhotoImage(file='Resources/passicon.png')
loginimage = PhotoImage(file="Resources/login.png")
registerimage = PhotoImage(file="Resources/register.png")
resetimage = PhotoImage(file="Resources/reset.png")
bg = Label(window, image=bgimage)
bg.pack()

'''Login contents'''
loginframe = LabelFrame(bg, text="", bg="white", width=500, height=600)
loginframe.place(x=75, y=75)

loginlabel = Label(window, text="LOGIN HERE", font=(
    "Rockwell Extra Bold", 23, "bold"), bg='white', fg='Red')
loginlabel.place(x=215, y=190)


'''username contents'''
vv = Label(window, image=loginicon)
vv.place(x=150, y=305)

usernamelable = Label(window, text="USERNAME:", font=(
    "Bahnschrift", 15, "bold"), bg='white')
usernamelable.place(x=150, y=270)

username = Entry(window, width=30, bg="silver", font=(8), fg="blue")
username.place(x=190, y=305)


'''password contents'''
vvv = Label(window, image=passicon)
vvv.place(x=150, y=405)

passwordlable = Label(window, text="PASSWORD:", font=(
    "Bahnschrift", 15, "bold"), bg='white',)
passwordlable.place(x=150, y=370)

password = Entry(window, width=30, bg="silver", font=(8), fg="blue", show='*')
password.place(x=190, y=405)


'''login button'''
loginbutton = Button(window, image=loginimage, cursor="hand2", command=lambda: login(
    str(username.get()), str(password.get())), bd=0)
loginbutton.place(x=260, y=478)

into = Label(window, text="With ♥ By BISHAL",
             font=("Candara", 10, "bold"), bg='white')
into.place(x=440, y=650)


window.mainloop()
