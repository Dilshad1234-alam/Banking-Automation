from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox, Treeview
import os,shutil
import time
from PIL import Image, ImageTk
import random
import tkinter as tk
import sql_tables
import sqlite3
import project_mails
from datetime import datetime, timedelta
# from tkintertable import TableCanvas, TableModel

#this function retur captcha
def generate_captcha():                               
    captcha=[]
    for i in range(3):
        c=chr(random.randint(65,90))
        captcha.append(c)

        n=random.randint(0,9)
        captcha.append(str(n))

    random.shuffle(captcha)
    captcha=' '.join(captcha)
    return captcha

def refresh():
    captcha=generate_captcha()
    captcha_lbl.configure(text=captcha)


root = Tk()                                          # create a window
root.state("zoomed")                                 # set  initial width & heirgt
root.config(bg="powder blue")              
root.title("ABC Bank")
root.resizable(width=False,height=False)

title=Label(root,text="Banking Automation",bg="powder blue",font=('Arial',50,"bold","underline"))
title.pack()

today=Label(root,text=time.strftime("%A,%d-%B-%Y"),bg="powder blue",font=('Arial',15,"bold"),fg="purple")     # Time create 
today.pack(pady=12)

img=Image.open("images/logo-bank.jpg").resize((300,180))   # create Image
img_bitmap=ImageTk.PhotoImage(img,master=root)

logo_lbl=Label(root,image=img_bitmap)
logo_lbl.place(relx=0,rely=0)

footer_lbl=Label(root,text="Developed By:xxxxxxxx",bg='powder blue',fg='purple',font=('Arial',20,"bold"))
footer_lbl.pack(side='bottom',pady=10)

def main_screen():                 # Create a Screen body
    def forgot():                  # create a forgot 
        frm.destroy()
        forgot_screen()

    def login():
        uacn=acn_entry.get()
        upass=pass_entry.get()
        ucap=inputcap_entry.get()
        utype=user_combo.get()
        actual_cap=captcha_lbl.cget("text")
        actual_cap=actual_cap.replace(' ','')

        if utype=="Admin":
            # admin_screen()
            if uacn=="0" and upass=="admin":     # and utype=="Admin"
                if ucap==actual_cap:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login','Invalid captcha')
            else:
                messagebox.showerror('Login','Invalid ACN/PASS/TYPE')
        elif utype=="User":
            if ucap==actual_cap:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=? and accounts_pass=?'
                curobj.execute(query,(uacn,upass))

                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("User Login","Invalid captcha")  
                else:
                    frm.destroy()
                    user_screen(uacn)             
            else:
                messagebox.showerror('Login','Invalid captcha')   
            # user_screen()
        else:
            messagebox.showerror("Login","Kindly select valid user Type")

    def toggle_password():
        if pass_entry.cget('show') == '':
            pass_entry.config(show='*')
            pass_entry.config(text='👁')  # Show eye icon
        else:
            pass_entry.config(show='')
            pass_entry.config(text='🙈')  # Show monkey icon (hidden)

    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)

    user_lbl=Label(frm,text="User Type",bg='pink',fg='black',font=('Arial',20,"bold"))
    user_lbl.place(relx=.3,rely=.1)

    user_combo=Combobox(frm,values=['Admin','User','----Select-----'],font=('',20),state="readonly")
    user_combo.current(2)
    user_combo.place(relx=.43,rely=.1)

    acn_lbl=Label(frm,text="ACN",bg='pink',font=('Arial',20,'bold'))
    acn_lbl.place(relx=.3,rely=.2)

    acn_entry=Entry(frm,font=('Arial',20),bd=5)
    acn_entry.place(relx=.43,rely=.2)
    acn_entry.focus()

    pass_lbl=Label(frm,text="PassWord",bg='pink',font=('Arial',20,'bold'))     # Password Lable
    pass_lbl.place(relx=.3,rely=.3)

    pass_entry=Entry(frm,font=('Arial',20),bd=5,show="*")        # Password Entry
    pass_entry.place(relx=.43,rely=.3)

    toggle_button =Button(frm, text='👁',font=('Arial',12),bg="#FFFFFF",bd=0 ,command=toggle_password)
    toggle_button.place(relx=.57,rely=.31)

    global captcha_lbl
    captcha_lbl=Label(frm,text=generate_captcha(),bg="#DCDCDC",font=('Arial',20,'bold'))
    captcha_lbl.place(relx=.43,rely=.4)

    refresh_btn=Button(frm,text="refresh",bg="purple",fg="white",command=refresh)
    refresh_btn.place(relx=.55,rely=.4)

    inputcap_lbl=Label(frm,text="Captcha",bg='pink',font=('Arial',20,'bold'))      # bg='pink'
    inputcap_lbl.place(relx=.3,rely=.5)

    inputcap_entry=Entry(frm,font=('Arial',20),bd=5)
    inputcap_entry.place(relx=.43,rely=.5)

    login_btn=Button(frm,text="login",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=login)
    login_btn.place(relx=.45,rely=.6)

    reset_btn=Button(frm,text="reset",bg="powder blue",font=('Arial',20,'bold'),bd=5)
    reset_btn.place(relx=.51,rely=.6)

    forgot_btn=Button(frm,width=18,text="forgot password",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=forgot)
    forgot_btn.place(relx=.43,rely=.72)



def admin_screen():                          # create  admin screen
    def open_acn():
        def open_acn_db():                     # database connection
            uname=name_entry.get()
            ufname=fname_entry.get()
            ugender=gender_combo.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            uaddress=address_entry.get()
            ubal=0.0
            uopendate=time.strftime("%A,%d-%B-%Y")
            upass=generate_captcha().replace(' ','')
                            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,ugender,ufname,uaddress,uopendate,ubal))
            conobj.commit()
            conobj.close()
            # messagebox.showinfo('open Account','Account opend successfully')
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query="select max(accounts_acno) from accounts"
            curobj.execute(query)

            uacno=curobj.fetchone()[0]
            curobj=conobj.cursor()


            try:
                project_mails.send_mail_for_openacn(uemail,uacno,uname,upass,uopendate)
                msg=f'Account opend with ACN {uacno} and mail sent to {uemail},Kindly check spam also'
                messagebox.showinfo('Open Account',msg)
            except Exception as msg:
                messagebox.showerror("Open Account",msg)
            

        def reset():
            name_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            gender_combo.delete(2)
            fname_entry.delete(0,"end")
            address_entry.delete(0,"end")
            name_entry.focus()
         

        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is open account screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack() 

        name_lbl=Label(ifrm,text="Full Name",bg='White',font=('Arial',20,'bold'))
        name_lbl.place(relx=.1,rely=.1)

        name_entry=Entry(ifrm,font=('Arial',20),bd=5)
        name_entry.place(relx=.1,rely=.18)
        name_entry.focus()

        fname_lbl=Label(ifrm,text="Father/Mother name",bg='White',font=('Arial',20,'bold'))
        fname_lbl.place(relx=.1,rely=.4)

        fname_entry=Entry(ifrm,font=('Arial',20),bd=5)
        fname_entry.place(relx=.1,rely=.48)

        gender_lbl=Label(ifrm,text="Gender",bg='White',font=('Arial',20,'bold'))
        gender_lbl.place(relx=.7,rely=.1)

        gender_combo=Combobox(ifrm,values=["Male","Female","Other","----Select------"],font=('Arial',20),state='readonly')
        gender_combo.current(3)
        gender_combo.place(relx=.7,rely=.18)

        mob_lbl=Label(ifrm,text="Mobile Number",bg='White',font=('Arial',20,'bold'))
        mob_lbl.place(relx=.4,rely=.1)

        mob_entry=Entry(ifrm,font=('Arial',20),bd=5)
        mob_entry.place(relx=.4,rely=.18)

        email_lbl=Label(ifrm,text="Email ID",bg='White',font=('Arial',20,'bold'))
        email_lbl.place(relx=.4,rely=.4)

        email_entry=Entry(ifrm,font=('Arial',20),bd=5)
        email_entry.place(relx=.4,rely=.48)

        address_lbl=Label(ifrm,text="Address",bg='White',font=('Arial',20,'bold'))
        address_lbl.place(relx=.7,rely=.4)

        address_entry=Entry(ifrm,font=('Arial',20),bd=5)
        address_entry.place(relx=.7,rely=.48)

        open_btn=Button(ifrm,text="open account",bg="green",font=('Arial',20,'bold'),fg="white",bd=5,command=open_acn_db)
        open_btn.place(relx=.38,rely=.7)

        reset_btn=Button(ifrm,text="reset",bg="green",font=('Arial',20,'bold'),fg="white",bd=5,command=reset)
        reset_btn.place(relx=.58,rely=.7)



    def delete_acn():               # create  delete screen 

        def send_otp():
            uacn=acn_entry.get()
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showerror("Delete Account", "Record not found")
            else:
                global otp, otp_generated_time          # Generate OTP & TIME
                otp=str(random.randint(1000,9999))
                otp_generated_time = datetime.now()
                otp_expire_time = otp_generated_time + timedelta(seconds=120)  # 2 minutes
                timer_running = True

                project_mails.send_otp(tup[3],tup[1],otp)  # Send OTP
                messagebox.showinfo('Delete Account','otp sent to registered mail id')

            otp_entry=Entry(ifrm,font=('Arial',20),bd=5)
            otp_entry.place(relx=.43,rely=.6)

             # Timer Label
            timer_lbl = Label(ifrm, font=('Arial', 12, 'bold'), bg='white', fg='red')
            timer_lbl.place(relx=.43, rely=.55)

             # Update Timer Function
            def update_timer():
                if not timer_running:
                    return

                remaining = (otp_expire_time - datetime.now()).total_seconds()
                if remaining <= 0:
                    timer_lbl.config(text="OTP expired!")
                    messagebox.showerror("Delete Account", "OTP expired. Please request again.")
                    return
                mins, secs = divmod(int(remaining), 60)
                timer_lbl.config(text=f"OTP Expires in: {mins:02}:{secs:02}")
                timer_lbl.after(1000, update_timer)

            update_timer()  # Start timer

            def verify():
                uotp=otp_entry.get()
                current_time = datetime.now()
                 # ✅ Check if OTP is expired (after 2 minutes)
                if (current_time - otp_generated_time).seconds > 120:
                    messagebox.showerror("Delete Account", "OTP expired. Please request again.")
                    return
            
                if otp==uotp:
                    resp= messagebox.askyesno("Delete Accounts", f"Do you want to delete this account?")
                    if not resp:
                       frm.destroy()
                       admin_screen()
                       return
                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    query='delete from accounts where accounts_acno=?'
                    curobj.execute(query,(uacn,))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Delete Account","Account Delete")
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Delete Account", "Incorrect OTP")

            verify_btn=Button(ifrm,text="verify",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=verify)
            verify_btn.place(relx=.69,rely=.58)

        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is delete account screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack()

        acn_lbl=Label(ifrm,text="ACN",bg='white',font=('Arial',20,'bold'))
        acn_lbl.place(relx=.3,rely=.2)

        acn_entry=Entry(ifrm,font=('Arial',20),bd=5)
        acn_entry.place(relx=.43,rely=.2)
        acn_entry.focus()

        otp_btn=Button(frm,text="Send OTP",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=send_otp)
        otp_btn.place(relx=.45,rely=.43)

    def view_acn():                     #create  view screen
        def view_details():
            uacn=acn_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("View Account", "Record not found")
            else:
                details=f""" User Name = {tup[1]}
Aval Bal = {tup[9]}
ACN Open date = {tup[8]}
Email = {tup[3]}
Mob = {tup[4]}
Father Name = {tup[6]}
Address = {tup[7]}
"""
                messagebox.showinfo("View Account",details)

        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is view account screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack()  

        acn_lbl=Label(ifrm,text="ACN",bg='white',font=('Arial',20,'bold'))
        acn_lbl.place(relx=.3,rely=.2)

        acn_entry=Entry(ifrm,font=('Arial',20),bd=5)
        acn_entry.place(relx=.43,rely=.2)
        acn_entry.focus()

        view_btn=Button(frm,text="View",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=view_details)
        view_btn.place(relx=.43,rely=.6)  

    def logout():
        resp=messagebox.askyesno("logout","Do you want to logout?")
        if resp:
            frm.destroy()
            main_screen()

    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)

    wel_lbl=Label(frm,text="Welcome,Admin",bg='pink',font=('Arial',20,'bold'),fg='green')      
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=logout)
    logout_btn.place(relx=.9,rely=0)

    open_btn=Button(frm,text="open account",bg="green",font=('Arial',20,'bold'),fg="white",bd=5,command=open_acn)
    open_btn.place(relx=.2,rely=0)

    delete_btn=Button(frm,text="delete account",bg="red",font=('Arial',20,'bold'),fg="white",bd=5,command=delete_acn)
    delete_btn.place(relx=.4,rely=0)

    view_btn=Button(frm,text="view account",bg="yellow",font=('Arial',20,'bold'),fg="black",bd=5,command=view_acn)
    view_btn.place(relx=.6,rely=0)

def forgot_screen():               # Forgot Password 
    def back():
        frm.destroy()
        main_screen()

    def send_otp():
        uacn=acn_entry.get()
        uemail=email_entry.get()
        ucaptcha=inputcap_entry.get()

        if ucaptcha!=forgot_captcha.replace(' ',''):
            messagebox.showerror('forgot password','Invalid captcha')
            return

        # authenticate acn & email
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? and accounts_email=?'
        curobj.execute(query,(uacn,uemail))
        tup=curobj.fetchone()
        curobj.close()

        if tup==None:
            messagebox.showerror("Forgot Password", "Record not found")
        else:
            global otp, otp_generated_time, timer_running
            otp=str(random.randint(1000,9999))
            otp_generated_time = datetime.now()
            otp_expire_time = otp_generated_time + timedelta(seconds=120)
            timer_running = True

            project_mails.send_otp(uemail,tup[1],otp)
            messagebox.showinfo('Forgot Pass','otp sent to given /registered mail id')

            otp_entry=Entry(frm,font=('Arial',20),bd=5)
            otp_entry.place(relx=.43,rely=.75)

               # Timer Label
            timer_lbl = Label(frm, font=('Arial', 12, 'bold'), bg='pink', fg='red')
            timer_lbl.place(relx=.43, rely=.7)

             # Countdown Function
            def update_timer():
                if not timer_running:
                    return

                remaining = (otp_expire_time - datetime.now()).total_seconds()
                if remaining <= 0:
                    timer_lbl.config(text="OTP expired!")
                    messagebox.showerror("Forgot Password", "OTP expired. Please request again.")
                    return
                mins, secs = divmod(int(remaining), 60)
                timer_lbl.config(text=f"OTP Expires in: {mins:02}:{secs:02}")
                timer_lbl.after(1000, update_timer)

            update_timer()  # Start countdown

            def verify():
                global timer_running
                uotp=otp_entry.get()
                current_time = datetime.now()

                if (current_time - otp_generated_time).seconds > 120:
                    messagebox.showerror("Forgot Password", "OTP expired. Please request again.")
                    return

                if otp==uotp:
                    timer_running = False
                    messagebox.showinfo("Forgot Password", f"Your Pass = {tup[2]} ")
                else:
                    messagebox.showerror("Forgot Password", "Incorrect OTP")

            verify_btn=Button(frm,text="verify",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=verify)
            verify_btn.place(relx=.65,rely=.75)

    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)

    back_btn=Button(frm,text="back",bg="powder blue",font=('Arial',20,'bold'),fg="black",bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    acn_lbl=Label(frm,text="ACN",bg='pink',font=('Arial',20,'bold'))
    acn_lbl.place(relx=.3,rely=.2)

    acn_entry=Entry(frm,font=('Arial',20),bd=5)
    acn_entry.place(relx=.43,rely=.2)
    acn_entry.focus()

    email_lbl=Label(frm,text="Email",bg='pink',font=('Arial',20,'bold'))
    email_lbl.place(relx=.3,rely=.3)

    email_entry=Entry(frm,font=('Arial',20),bd=5)
    email_entry.place(relx=.43,rely=.3)

    global captcha_lbl
    forgot_captcha=generate_captcha()
    captcha_lbl=Label(frm,text=forgot_captcha,bg="white",font=('Arial',20,'bold'))
    captcha_lbl.place(relx=.43,rely=.4)

    refresh_btn=Button(frm,text="refresh",bg="purple",fg="white",command=refresh)
    refresh_btn.place(relx=.55,rely=.4)

    inputcap_entry=Entry(frm,font=('Arial',20),bd=5)
    inputcap_entry.place(relx=.43,rely=.5)

    otp_btn=Button(frm,text="Send OTP",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=send_otp)
    otp_btn.place(relx=.43,rely=.6)

    reset_btn=Button(frm,text="reset",bg="powder blue",font=('Arial',20,'bold'),bd=5)
    reset_btn.place(relx=.52,rely=.6)

def user_screen(uacn=None):                   # create user screen
    def logout():
        resp=messagebox.askyesno("logout","Do you want to logout?")
        if resp:
            frm.destroy()
            main_screen()
    
    
    def update_btn_screen():
        def update_db():
            uname=name_entry.get()
            upass=pass_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            ufname=fname_entry.get()
            uaddress=address_entry.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query='Update accounts set accounts_name=?,accounts_pass=?,accounts_email=?,accounts_mob=?,accounts_fname=?,accounts_address=? where accounts_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,ufname,uaddress,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Details","Profile Updated")
            frm.destroy()
            admin_screen()
            user_screen(uacn)

        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.65)

        title_lbl=Label(ifrm,text="This is update screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack()  
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        name_lbl=Label(ifrm,text="Name",bg='White',font=('Arial',20,'bold'))
        name_lbl.place(relx=.1,rely=.1)

        name_entry=Entry(ifrm,font=('Arial',20),bd=5)
        name_entry.place(relx=.1,rely=.18)
        name_entry.insert(0,tup[1])
        name_entry.focus()

        fname_lbl=Label(ifrm,text="Father/Mother name",bg='White',font=('Arial',20,'bold'))
        fname_lbl.place(relx=.1,rely=.4)

        fname_entry=Entry(ifrm,font=('Arial',20),bd=5)
        fname_entry.place(relx=.1,rely=.48)
        fname_entry.insert(0,tup[6])

        pass_lbl=Label(ifrm,text="Password",bg='White',font=('Arial',20,'bold'))
        pass_lbl.place(relx=.7,rely=.1)

        pass_entry=Entry(ifrm,font=('Arial',20),bd=5)
        pass_entry.place(relx=.7,rely=.18)
        pass_entry.insert(0,tup[2])

        mob_lbl=Label(ifrm,text="Mobile Number",bg='White',font=('Arial',20,'bold'))
        mob_lbl.place(relx=.4,rely=.1)

        mob_entry=Entry(ifrm,font=('Arial',20),bd=5)
        mob_entry.place(relx=.4,rely=.18)
        mob_entry.insert(0,tup[4])

        email_lbl=Label(ifrm,text="Email ID",bg='White',font=('Arial',20,'bold'))
        email_lbl.place(relx=.4,rely=.4)

        email_entry=Entry(ifrm,font=('Arial',20),bd=5)
        email_entry.place(relx=.4,rely=.48)
        email_entry.insert(0,tup[3])

        address_lbl=Label(ifrm,text="Address",bg='White',font=('Arial',20,'bold'))
        address_lbl.place(relx=.7,rely=.4)

        address_entry=Entry(ifrm,font=('Arial',20),bd=5)
        address_entry.place(relx=.7,rely=.48)
        address_entry.insert(0,tup[7])

        update_btn=Button(ifrm,text="update",bg="powder blue",font=('Arial',20,'bold'),fg="black",bd=5,command=update_db)
        update_btn.place(relx=.38,rely=.7) 

    def check_btn_screen():
        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.65)

        title_lbl=Label(ifrm,text="This is details screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack() 

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        details=f'''Account No. = {tup[0]}

                Availabale Bal = {tup[9]}

                Opening date = {tup[8]}

                Email ID = {tup[3]}

                Mob No. = {tup[4]}

                Father Name = {tup[6]}

                Address = {tup[7]}
            '''
        
        details_lbl=Label(ifrm,bg='white',text=details,fg='purple',font=('arial', 20, 'bold'))
        details_lbl.place(relx=.2,rely=.14)

    def deposit_btn_screen():
        def deposit():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='Update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
            curobj.execute(query,(uamt,uacn,))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()
            
            t=str(time.time())                        #  Transaction ID
            utxnid='txn'+t[:t.index('.')]                      
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into stmts values(?,?,?,?,?,?)'
            curobj.execute(query,(uacn,uamt,'CR.',time.strftime("%d-%m-%Y-%r"),ubal,utxnid))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit",f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn)


        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.65)

        title_lbl=Label(ifrm,text="This is deposit screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack() 

        amt_lbl=Label(ifrm,text="Amount",bg='white',font=('Arial',20,'bold'))
        amt_lbl.place(relx=.3,rely=.2)

        amt_entry=Entry(ifrm,font=('Arial',20),bd=5)
        amt_entry.place(relx=.43,rely=.2)
        amt_entry.focus()

        dep_btn=Button(frm,text="deposit",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=deposit)
        dep_btn.place(relx=.45,rely=.43)


    def withdraw_btn_screen():
        def withdraw():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='Update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()

                t=str(time.time())                        #  Transaction ID
                utxnid='txn'+t[:t.index('.')]                      
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='insert into stmts values(?,?,?,?,?,?)'
                curobj.execute(query,(uacn,uamt,'DB.',time.strftime("%d-%m-%Y-%r"),ubal-uamt,utxnid))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdraw",f"{uamt} Amount Withdrawn")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Withdraw","Insufficient Bal {ubal}")

        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.65)

        title_lbl=Label(ifrm,text="This is withdraw screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack() 

        amt_lbl=Label(ifrm,text="Amount",bg='white',font=('Arial',20,'bold'))
        amt_lbl.place(relx=.3,rely=.2)

        amt_entry=Entry(ifrm,font=('Arial',20),bd=5)
        amt_entry.place(relx=.43,rely=.2)
        amt_entry.focus()

        dep_btn=Button(frm,text="Withdraw",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=withdraw)
        dep_btn.place(relx=.45,rely=.43)
        
         

    def transfer_btn_screen():
        def transfer():
            toacn=to_entry.get()
            uamt=float(amt_entry.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(toacn,))
            to_tup=curobj.fetchone()
            conobj.close()

            if to_tup==None:
                messagebox.showerror("Transfer","To ACN des not exist")
                return
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()
            
            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query_deduct='Update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                query_credit='Update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'

                curobj.execute(query_deduct,(uamt,uacn))
                curobj.execute(query_credit,(uamt,toacn))

                conobj.commit()
                conobj.close()

                t=str(time.time())                        #  Transaction ID
                utxnid1='txn_db'+t[:t.index('.')]   
                utxnid2='txn_cr'+t[:t.index('.')]

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='insert into stmts values(?,?,?,?,?,?)'
                query2='insert into stmts values(?,?,?,?,?,?)'

                curobj.execute(query1,(uacn,uamt,'DB.',time.strftime("%d-%m-%Y-%r"),ubal-uamt,utxnid1))
                # time.sleep(1)
                curobj.execute(query2,(toacn,uamt,'CR.',time.strftime("%d-%m-%Y-%r"),ubal+uamt,utxnid2))
                
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Transfer",f"{uamt} Amount Transferred")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Transfer",f"Insufficient Bal {ubal}")

     

        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.65)

        title_lbl=Label(ifrm,text="This is transfer screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack() 

        to_lbl=Label(ifrm,text="TO ACN",bg='white',font=('Arial',20,'bold'))
        to_lbl.place(relx=.3,rely=.2)

        to_entry=Entry(ifrm,font=('Arial',20),bd=5)
        to_entry.place(relx=.43,rely=.2)
        to_entry.focus()

        amt_lbl=Label(ifrm,text="Amount",bg='white',font=('Arial',20,'bold'))
        amt_lbl.place(relx=.3,rely=.4)

        amt_entry=Entry(ifrm,font=('Arial',20),bd=5)
        amt_entry.place(relx=.43,rely=.4)

        tr_btn=Button(frm,text="transfer",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=transfer)
        tr_btn.place(relx=.5,rely=.6)

    def history_btn_screen():
        ifrm=Frame(frm,highlightcolor='black',highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.65)

        title_lbl=Label(ifrm,text="This is history screen",bg='white',font=('Arial',20,'bold'),fg='purple')      
        title_lbl.pack() 

        columns = ("Txn ID", "Amount", "Txn Type", "Update Bal", "Date")
        tree = Treeview(ifrm, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill='both', expand=True)

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        curobj.execute(
            '''SELECT stmts_txnid, stmts_amt, stmts_type, stmts_Update_bal, stmts_date 
            FROM stmts WHERE stmts_acn=?''', (uacn,))
        for row in curobj.fetchall():
            tree.insert("", "end", values=row)

        conobj.close()

    def getdetails():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=?'
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        return tup

    def update_picture():
        # def update_picture():
        path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )

        if path:  # ✅ Proceed only if a file is selected
            try:
                # Check if images folder exists
                if not os.path.exists("images"):
                    os.makedirs("images")

                # Copy image
                shutil.copy(path, f"images/{uacn}.png")

                # Show image
                profile_img = Image.open(f"images/{uacn}.png").resize((210, 180))
                bitmap_profile_img = ImageTk.PhotoImage(profile_img, master=root)
                profile_img_lbl = Label(frm, image=bitmap_profile_img)
                profile_img_lbl.image = bitmap_profile_img
                profile_img_lbl.configure(image=bitmap_profile_img)

            except Exception as e:
                messagebox.showerror("Error", f"Image update failed:\n{e}")
        else:
            messagebox.showwarning("No Image Selected", "Please select an image to upload.")



        # path=filedialog.askopenfilename()
        # shutil.copy(path,f"images/{uacn}.png")

        # profile_img=Image.open(f"images/{uacn}.png").resize((210,180))
        # bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
        # profile_img_lbl=Label(frm,image=bitmap_profile_img)
        # profile_img_lbl.image=bitmap_profile_img
        # profile_img_lbl.configure(image=bitmap_profile_img)

    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)

    wel_lbl=Label(frm,text=f"Welcome,{getdetails()[1]}",bg='pink',font=('Arial',20,'bold'),fg='green')      
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",bg="powder blue",font=('Arial',20,'bold'),bd=5,command=logout)
    logout_btn.place(relx=.92,rely=0)
    if os.path.exists(f'images/{uacn}.png'):
        path=f"images/{uacn}.png"
    else:
        path="images/default-pic.jpg"

    profile_img=Image.open(path).resize((210,180))
    bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
    profile_img_lbl=Label(frm,image=bitmap_profile_img)
    profile_img_lbl.image=bitmap_profile_img
    profile_img_lbl.place(relx=.005,rely=.05)

    update_pic_btn=Button(frm,text="update pic",width=10,bg="powder blue",font=('Arial',20,'bold'),bd=5,fg="black",command=update_picture)
    update_pic_btn.place(relx=.005,rely=.3)

    check_btn=Button(frm,text="check details",width=10,bg="Yellow",font=('Arial',20,'bold'),bd=5,fg="black",command=check_btn_screen)
    check_btn.place(relx=.005,rely=.4)

    deposit_btn=Button(frm,text="deposit",width=10,bg="green",font=('Arial',20,'bold'),bd=5,fg="black",command=deposit_btn_screen)
    deposit_btn.place(relx=.005,rely=.5)

    withdraw_btn=Button(frm,text="withdraw",width=10,bg="red",font=('Arial',20,'bold'),bd=5,fg="black",command=withdraw_btn_screen)
    withdraw_btn.place(relx=.005,rely=.6)

    update_btn=Button(frm,text="update",width=10,bg="yellow",font=('Arial',20,'bold'),bd=5,fg="black",command=update_btn_screen)
    update_btn.place(relx=.005,rely=.7)

    transfer_btn=Button(frm,text="transfer",width=10,bg="red",font=('Arial',20,'bold'),bd=5,fg="black",command=transfer_btn_screen)
    transfer_btn.place(relx=.005,rely=.8)

    history_btn=Button(frm,text="history",width=10,bg="green",font=('Arial',20,'bold'),bd=5,fg="black",command=history_btn_screen)
    history_btn.place(relx=.005,rely=.9)
    
main_screen()
root.mainloop()   
