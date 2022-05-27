from tkinter import *
from tkinter import messagebox
import pymysql
import credentials as cr
from subprocess import call



    

def login_func():
    if email_entry.get()=="" or password_entry.get()=="":
        messagebox.showerror("Error!","All fields are required",parent=window)
    else:
        try:
            connection=pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            cur.execute("select * from student_register where email=%s and password=%s",(email_entry.get(),password_entry.get()))
            row=cur.fetchone()
            if row == None:
                messagebox.showerror("Error!","Invalid USERNAME & PASSWORD",parent=window)
            else:
                messagebox.showinfo("Success","Wellcome to the PySeek family",parent=window)
                reset_fields()
                f=open("a.txt","w")
                f.write(str(row))
                f.close()
                connection.close()
                window.destroy()
                call(["python","tictactoe.py"])
                
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=window)





def redirect_window():
    window.destroy()
    call(["python","signup_page.py"])
    root.mainloop()

def reset_fields():
    email_entry.delete(0,END)
    password_entry.delete(0,END)

# The main function


if __name__ == "__main__":
    root = Tk()
    window = root
    window.title("Log In PySeek")
    window.geometry("1280x800+0+0")
    window.config(bg = "white")

    frame1 = Frame(window, bg="yellow")
    frame1.place(x=0, y=0, width=450, relheight = 1)

    label1 = Label(frame1, text= "Py", font=("times new roman", 40, "bold"), bg="yellow", fg="red").place(x=100,y=300)
    label2 = Label(frame1, text= "Seek", font=("times new roman", 40, "bold"), bg="yellow", fg="RoyalBlue1").place(x=162,y=300)
    label3 = Label(frame1, text= "It's all about Python", font=("times new roman", 13, "bold"), bg="yellow", fg="brown4").place(x=100,y=360)

    frame2 = Frame(window, bg = "gray95")
    frame2.place(x=450,y=0,relwidth=1, relheight=1)

    frame3 = Frame(frame2, bg="white")
    frame3.place(x=140,y=150,width=500,height=450)

    email_label = Label(frame3,text="Email Address", font=("helvetica",20,"bold"),bg="white", fg="gray").place(x=50,y=40)
    email_entry = Entry(frame3,font=("times new roman",15,"bold"),bg="white",fg="gray")
    email_entry.place(x=50, y=80, width=300)

    password_label = Label(frame3,text="Password", font=("helvetica",20,"bold"),bg="white", fg="gray").place(x=50,y=120)
    password_entry = Entry(frame3,font=("times new roman",15,"bold"),bg="white",fg="gray",show="*")
    password_entry.place(x=50, y=160, width=300)

    login_button = Button(frame3,text="Log In",command=login_func,font=("times new roman",15, "bold"),bd=0,cursor="hand2",bg="blue",fg="white").place(x=50,y=200,width=300)

    create_button = Button(frame3,text="Create New Account",command=redirect_window,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="green2",fg="white").place(x=80,y=320,width=250)

    root.mainloop()
