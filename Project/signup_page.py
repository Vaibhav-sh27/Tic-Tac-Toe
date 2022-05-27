from tkinter import *
from PIL import ImageTk
from tkinter import messagebox,ttk
import pymysql
import credentials as cr
from subprocess import call
import smtplib, ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
    
def signup_func():
    spc='!@#$%^&*()_+=-?/,<>'
    if fname_txt.get()=="" or lname_txt.get()=="" or email_txt.get()=="" or password_txt.get() == "":
        messagebox.showerror("Error!","Sorry!, All fields are required",parent=window)
    
    elif '@'not in email_txt.get():
        messagebox.showerror("Error!","Please Enter a valid email id",parent=window)
    elif otp_txt.get()!=tp:
        messagebox.showerror("Error!","Invalid OTP",parent=window)
    elif len(password_txt.get())<8 or not(any(c in spc for c in password_txt.get())) or not(any(c.isdigit() for c in password_txt.get())) or fname_txt.get() in password_txt.get():
        messagebox.showerror("Error!","Please Enter a valid Password\n\nYour Password should contain atleast :\n8 characters\n1 digit\n1 special character\nShould not contain your Name",parent=window)
    elif terms.get() == 0:
        messagebox.showerror("Error!","Please Agree with our Terms & Conditions",parent=window)
    else:
        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            cur.execute("select * from student_register where email=%s",email_txt.get())
            row=cur.fetchone()

            # Check if th entered email id is already exists or not.
            if row!=None:
                messagebox.showerror("Error!","The email id is already exists, please try again with another email id",parent=window)
            else:
                cur.execute("insert into student_register (f_name,l_name,email,password) values(%s,%s,%s,%s)",
                                (
                                    fname_txt.get(),
                                    lname_txt.get(),
                                    email_txt.get(),
                                    password_txt.get()
                                ))
                connection.commit()
                cur.execute("select * from student_register where email=%s",email_txt.get())
                row=cur.fetchone()
                f=open("a.txt","w")
                f.write(str(row))
                f.close()
                connection.close()
                messagebox.showinfo("Congratulations!","Register Successful",parent=window)
                reset_fields()
                window.destroy()
                call(["python","tictactoe.py"])
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=window)

def send_otp():
    global tp
    tp=''
    for i in range(4):
        tp+=str(random.randrange(0,9))
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = ' vaibhavshrotriyas@gmail.com '  # Enter your address
        receiver_email = email_txt.get()  # Enter receiver address
        password =' 231059102876 '
        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome To Pyseek!"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
        Hi,
        Your OTP is {tp}"""

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")


        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server,port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=window)


def reset_fields():
    fname_txt.delete(0, END)
    lname_txt.delete(0, END)
    email_txt.delete(0, END)
    password_txt.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    window = root
    window.title("Sign Up")
    window.geometry("1280x800+0+0")
    window.config(bg = "white")

    bg_img = ImageTk.PhotoImage(file="photo1.jpeg")
    background = Label(window,image=bg_img).place(x=0,y=0,relwidth=1,relheight=1)

    frame = Frame(window, bg="white")
    frame.place(x=350,y=100,width=500,height=550)

    title1 = Label(frame, text="Sign Up", font=("times new roman",25,"bold"),bg="white").place(x=20, y=10)
    title2 = Label(frame, text="Join with us", font=("times new roman",13),bg="white", fg="gray").place(x=20, y=50)

    f_name = Label(frame, text="First name", font=("helvetica",15,"bold"),bg="white").place(x=20, y=100)
    l_name = Label(frame, text="Last name", font=("helvetica",15,"bold"),bg="white").place(x=240, y=100)

    fname_txt = Entry(frame,font=("arial"))
    fname_txt.place(x=20, y=130, width=200)

    lname_txt = Entry(frame,font=("arial"))
    lname_txt.place(x=240, y=130, width=200)

    email = Label(frame, text="Email", font=("helvetica",15,"bold"),bg="white").place(x=20, y=180)

    email_txt = Entry(frame,font=("arial"))
    email_txt.place(x=20, y=210, width=420)

    #sec_question = Label(frame, text="Security questions", font=("helvetica",15,"bold"),bg="white").place(x=20, y=260)
    answer = Label(frame, text="Enter OTP", font=("helvetica",15,"bold"),bg="white").place(x=20, y=260)

    otp = Button(frame,text="Send OTP",command=send_otp,font=("times new roman",15, "bold"),bd=0,cursor="hand2",bg="green2",fg="white")
    otp.place(x=240, y=290,width=100)

    otp_txt = Entry(frame,font=("arial"))
    otp_txt.place(x=20, y=290, width=200)

    password =  Label(frame, text="New password", font=("helvetica",15,"bold"),bg="white").place(x=20, y=340)

    password_txt = Entry(frame,font=("arial"))
    password_txt.place(x=20, y=370, width=420)


    terms = IntVar()
    terms_and_con = Checkbutton(frame,text="I Agree The Terms & Conditions",variable=terms,onvalue=1,offvalue=0,bg="white",font=("times new roman",12)).place(x=20,y=420)
    signup = Button(frame,text="Sign Up",command=signup_func,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="green2",fg="white").place(x=120,y=470,width=250)

    root.mainloop()
