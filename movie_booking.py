import customtkinter as ctk
import mysql.connector as mysql
from PIL import Image, ImageTk
from datetime import date

seat_Dictionary={}

con=mysql.connect(host="localhost",username="root",password="Harsha@1234",database="comp_project")
cur=con.cursor()

cur.execute("select * from log_in_info;")
log_in_info=cur.fetchall()
data_login=[]
for i in log_in_info:
    data_login.append([i[0],i[1]])

cur.execute("select * from list_movies;")
list_movies = cur.fetchall()
list_movies_data = []
for i in list_movies:
    list_movies_data.append([i[0],i[1],i[2]])


app = ctk.CTk()
ctk.set_appearance_mode("dark")
app.geometry("500x500")
app.title("trail")



#Change Frames
def change(frame1,frame2):
    frame2.pack(fill="both",expand=True)
    frame1.pack_forget()

def log_in_def():
    global log_in_info
    global number
    username = l_username_str.get()
    password = l_password_str.get()
    if [username,password] in data_login:
        global home_page
        number=1
        change(log_in,home_page)
        label_home = ctk.CTkLabel(master=home_page,text="Home Page",font=("Agency FB",24,"bold"))
        home_button = ctk.CTkButton(master=home_page,text="Book A ticket",command=book_ticket)
        myactitvity_button = ctk.CTkButton(master=home_page,text="My Activities",command=lambda: my_activity(username))

        label_home.pack()
        home_button.pack(pady=10)
        myactitvity_button.pack()
        home_page.pack(fill="both",expand=True)

def sign_up_def():
    username = s_username_str.get()
    password = s_password_str.get()
    cpassword = s_cpassword_str.get()
    mail_ID  = s_mailid_str.get()
    if(password==cpassword):
        cur.execute(f"insert into log_in_info values('{username}','{password}','{mail_ID}');")
        cur.execute(f"create table {username}(BDATE date,movie_code varchar(13),movie_name varchar(20));")
        con.commit()
        change(sign_up,home_page)
        label_home = ctk.CTkLabel(master=home_page,text="Home Page",font=("Agency FB",24,"bold"))
        home_button = ctk.CTkButton(master=home_page,text="Book A ticket",command=book_ticket)
        myactitvity_button = ctk.CTkButton(master=home_page,text="My Activities",command=lambda: my_activity(username))

        label_home.pack()
        home_button.pack(pady=10)
        myactitvity_button.pack()
        home_page.pack(fill="both",expand=True)
        number=2
def my_activity(username):
    my_activity_frame = ctk.CTkFrame(app)
    change(home_page,my_activity_frame)
    cur.execute(f"select * from {username}")
    activity_data = cur.fetchall()
    for i in range(0,4):
        movie_name_a = ctk.CTkLabel(my_activity_frame,text=f"MOVIE NAME:{activity_data[i][1]}",font=("Agency FB",20,"bold"))
        movie_code_a = ctk.CTkLabel(my_activity_frame,text=f"MOVIE CODE:{activity_data[i][2]}",font=("Agency FB",20,"bold"))
        date_activity = ctk.CTkLabel(my_activity_frame,text=f"DATE:{activity_data[i][0]}",font=("Agency FB",20,"bold"))
        space_label = ctk.CTkLabel(my_activity_frame,text="")
        movie_name_a.pack()
        movie_code_a.pack()
        date_activity.pack()
        space_label.pack()

number=0

def add(movie_code,movie_name,price_int,add_movie_frame,admin_frame):
    movie_code_str = movie_code.get()
    movie_name_str = movie_name.get()
    price = price_int.get()
    cur.execute(f"insert into list_movies values('{movie_code_str}','{movie_name_str}',{price})")
    cur.execute(f"create table {movie_name_str}(seats varchar(200));")
    cur.execute(f"insert into {movie_name_str} values('[0]');")
    con.commit()
    movie_succ_frame = ctk.CTkFrame(app)
    change(add_movie_frame,movie_succ_frame)
    done_label = ctk.CTkLabel(movie_succ_frame,text="DONE",font=("Agenncy FB",50,"bold"))
    done_label.pack(anchor="center")
    back_button = ctk.CTkButton(movie_succ_frame,text="Admin page",command=lambda:change(movie_succ_frame,admin_frame))
    back_button.pack()

def add_movie(admin_frame):
    global cur
    add_movie_frame = ctk.CTkFrame(app)
    change(admin_frame,add_movie_frame)
    add_movie_label = ctk.CTkLabel(add_movie_frame,text="ADD A MOVIE",font=("Agency FB",20,"bold"))
    movie_code = ctk.StringVar()
    movie_name = ctk.StringVar()
    price_int = ctk.IntVar()
    movie_code_entry = ctk.CTkEntry(add_movie_frame,textvariable=movie_code)
    movie_name_entry = ctk.CTkEntry(add_movie_frame,textvariable=movie_name)
    price_entry = ctk.CTkEntry(add_movie_frame,textvariable=price_int)
    add_movie_button = ctk.CTkButton(add_movie_frame,text="ADD",command=lambda:add(movie_code,movie_name,price_int,add_movie_frame,admin_frame))
    add_movie_label.pack(pady=5)
    movie_code_entry.pack(pady=5)
    movie_name_entry.pack(pady=5)
    price_entry.pack(pady=5)
    add_movie_button.pack(pady=5)

def admin_login():
    global cur
    cur.execute("select * from admin_info;")
    admin_info = cur.fetchall()
    admin_info_data = []
    for i in admin_info:
        admin_info_data.append(i)
    username = l_username_str.get()
    password = l_password_str.get()
    if(username,password) in admin_info_data:
        admin_frame = ctk.CTkFrame(app)
        change(log_in,admin_frame)
        admin_page_label = ctk.CTkLabel(admin_frame,text="ADMIN PAGE",font=("Agency FB",20,"bold"))
        add_a_movie = ctk.CTkButton(admin_frame,text="Add A Movie",command=lambda:add_movie(admin_frame))
        admin_page_label.pack()
        add_a_movie.pack()

    

#Frames....

log_in = ctk.CTkFrame(master=app)
sign_up = ctk.CTkFrame(master=app)
home_page = ctk.CTkFrame(master=app)
book_ticket_frame = ctk.CTkFrame(app)



#For login....

l_username_str = ctk.StringVar()
l_password_str = ctk.StringVar()
l_username=ctk.CTkEntry(master=log_in,placeholder_text="Username",textvariable=l_username_str)
l_password=ctk.CTkEntry(master=log_in,placeholder_text="password",textvariable=l_password_str)
l_str=ctk.CTkLabel(master=log_in,text="Login Menu",font=("Agency FB",20,"bold"))
l_button=ctk.CTkButton(master=log_in,text="Login",command=log_in_def)
l_admin_button = ctk.CTkButton(log_in,text="Admin Login",command=admin_login)
l_str.pack()
l_username.pack(pady=5)
l_password.pack(pady=5)
l_button.pack(pady=5)
l_admin_button.pack(pady=5)


label2=ctk.CTkLabel(master=log_in,text="Dont have an account?")
button2=ctk.CTkButton(master=log_in,text="Sign UP",command= lambda: change(log_in,sign_up),width=70,height=24)
label2.pack(pady=5)
button2.pack()
log_in.place(relx=0.5,rely=0.5,anchor="center")







#For Sign up....



s_username_str = ctk.StringVar()
s_password_str = ctk.StringVar()
s_cpassword_str = ctk.StringVar()
s_mailid_str = ctk.StringVar()

s_label = ctk.CTkLabel(sign_up,text="SIGN IN",font=("Agency FB",20,"bold"))
s_username = ctk.CTkEntry(master=sign_up,placeholder_text="Username",textvariable=s_username_str)
s_mailid = ctk.CTkEntry(master=sign_up,placeholder_text="Mail ID",textvariable=s_mailid_str)
s_password = ctk.CTkEntry(master=sign_up,placeholder_text="password",textvariable=s_password_str)
s_cpassword = ctk.CTkEntry(master=sign_up,placeholder_text="confirm password",textvariable=s_cpassword_str)
s_sign_up = ctk.CTkButton(master=sign_up,text="Sign Up",command=sign_up_def)


s_label.pack()
s_username.pack(pady=5)
s_mailid.pack(pady=5)
s_password.pack(pady=5)
s_cpassword.pack(pady=5)
s_sign_up.pack(pady=5)



#HOMEPAGE....






def book_ticket():
    global list_movies_data
    global price
    change(home_page,book_ticket_frame)
    list_mov = ctk.CTkLabel(book_ticket_frame,text="List of Movies",font=("Agency FB",30,"bold"))
    no_of_movies = len(list_movies_data)
    list_mov.pack()
    for i in range(no_of_movies):
        movie_code = list_movies_data[i][0]
        movie_name = list_movies_data[i][1]
        price = list_movies_data[i][2]
        movie_frame = ctk.CTkFrame(book_ticket_frame,width=100,height=100)
        movie_label_name = ctk.CTkLabel(movie_frame,text=f"Movie Name:  {movie_name}",font=("Agency FB",20))
        movie_label_code = ctk.CTkLabel(movie_frame,text=f"Movie Code:  {movie_code}",font=("Agency FB",20))
        price_label = ctk.CTkLabel(movie_frame,text=f"Price: {price}",font=("Agency FB",20))
        movie_button = ctk.CTkButton(movie_frame,text="BOOK",command=lambda: book_seats(movie_code,movie_name,book_ticket_frame))
        movie_label_name.pack()
        movie_label_code.pack()
        price_label.pack()
        movie_button.pack()
        movie_frame.pack(pady=10)
price=0
       
def show(movie_code,movie_name):
    ticket_book_frame = ctk.CTkFrame(app)
    change(book_ticket_frame,ticket_book_frame)
    movie_name_label = ctk.CTkLabel(ticket_book_frame,text=f"{movie_name}",font=("Agency FB",30,"bold"))
    no_seats_entry_str = ctk.StringVar()
    no_seats_entry = ctk.CTkEntry(ticket_book_frame,textvariable=no_seats_entry_str)
    no_seats_label = ctk.CTkLabel(ticket_book_frame,text="No.of Seats:")
    sub=ctk.CTkButton(ticket_book_frame,text="Book Ticket",command=lambda f=ticket_book_frame,seats=no_seats_entry_str,movie_code=movie_code: book_seats(no_seats_entry_str,movie_code,f))
    ticket_book_frame.rowconfigure(0,weight=10)
    ticket_book_frame.rowconfigure(1,weight=1)
    ticket_book_frame.rowconfigure(2,weight=1)
    ticket_book_frame.rowconfigure(3,weight=1)
    ticket_book_frame.rowconfigure(4,weight=10)
    ticket_book_frame.columnconfigure(0,weight=10)
    ticket_book_frame.columnconfigure(1,weight=1)
    ticket_book_frame.columnconfigure(2,weight=1)
    ticket_book_frame.columnconfigure(3,weight=1)
    ticket_book_frame.columnconfigure(4,weight=10)
    movie_name_label.grid(column=2,row=1)
    no_seats_label.grid(column=1,row=2)
    no_seats_entry.grid(column=2,row=2)
    sub.grid(column=2,row=3)


def book_seats(movie_code,movie_name,book_ticket_frame):
    seats_frame = ctk.CTkFrame(app)
    global seat_Dictionary
    global seats_Booked
    cur.execute(f"select * from {movie_name}")
    seats_data = cur.fetchall()
    seats_Booked=[]
    for i in seats_data:
        for j in i:
            seats_Booked_str=j[1:-1].split(",")
    for i in seats_Booked_str:
        seats_Booked.append(int(i))
    change(book_ticket_frame,seats_frame)
    seats_frame.columnconfigure(0,weight=1)
    for i in range(1,11):
        seats_frame.columnconfigure(i,weight=1)
    seats_frame.columnconfigure(11,weight=1)
    seats_frame.rowconfigure(0,weight=1)
    for i in range(1,11):
        seats_frame.rowconfigure(i,weight=1)
    seats_frame.rowconfigure(11,weight=1)
    n=1
    for i in range(1,11):
        for j in range(1,11):
            if(n in seats_Booked):
                n+=1
            else:
                button=ctk.CTkButton(seats_frame,text=f'{n}',command=lambda n=n:addSeat(n,),fg_color="#0000FF")
                seat_Dictionary[str(n)]=button
                button.grid(column=i,row=j)
                n+=1
    book_button = ctk.CTkButton(seats_frame,text="BOOK",command = lambda:payment(seats_frame,movie_code,movie_name))
    book_button.grid(column=6,row=11)



def addSeat(n):
    global nbooked
    nbooked+=1
    global seat_Dictionary
    global seats_Booked
    if n not in seats_Booked:
        seat_Dictionary[str(n)].configure(fg_color="#FFF")
        seats_Booked.append(n)
    else:
        seats_Booked.remove(n)
        seat_Dictionary[str(n)].configure(fg_color="#0000FF")

nbooked=0
def payment(seats_frame,movie_name,movie_code):
    global seats_Booked
    global number
    global price
    global nbooked
    payment_frame = ctk.CTkFrame(app)
    change(seats_frame,payment_frame)  
    image_original = Image.open("C:/Users/lenovo/Desktop/qrcode.png")
    payment_label = ctk.CTkLabel(payment_frame,text="PAYMENT",font=("Agency FB",20,"bold"))



    
    image_tk = ctk.CTkImage(light_image=Image.open("C:/Users/lenovo/Desktop/qrcode.png"),size=(300,300))
    payment_qr_code_label = ctk.CTkLabel(payment_frame,image=image_tk,text="")
    payment_price  = ctk.CTkLabel(payment_frame,text=f"Total Cost={nbooked*price}",font=("Agency FB",20,"bold"))
    payment_label.pack()
    payment_qr_code_label.pack()
    payment_price.pack()
    if(number==1):
        username = l_username_str.get()
        cur.execute(f"insert into {username} values ('{date.today()}','{movie_code}','{movie_name}')")
        con.commit()
    else:
        username = s_username_str.get()
        cur.execute(f"insert into {username} values ('{date.today()}','{movie_code}','{movie_name}')")
        con.commit()
    cur.execute(f"delete from {movie_code};")
    cur.execute(f"insert  into {movie_code} values ('{seats_Booked}')")
    con.commit()

seats_Booked=[]



app.mainloop()