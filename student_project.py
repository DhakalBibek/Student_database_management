from tkinter import Tk,Label,Button,END,StringVar,Entry,Frame,GROOVE,RIDGE,Grid,ttk,Text,Scrollbar,HORIZONTAL,VERTICAL,BOTH,BOTTOM,X,RIGHT,Y,messagebox
#-----install pymysql first --- perform (pip install pymysql) 

import pymysql


class student:
    def __init__(self,base):
        self.base=base
        self.base.title("Bibek_Dhakal(KCE074BEL011)")
        self.width_value=base.winfo_screenwidth()
        self.height_value=base.winfo_screenheight()
        self.base.geometry("1200x700+150+50")
        self.base.resizable(0,0) 
    
        
        Label(self.base,text="Student Database Management System",font=("Times",32,"bold"),fg="blue",bg="lavender",bd=10,relief=GROOVE).pack()

        #all data variables

        self.Rollno_var=StringVar()
        self.Name_var=StringVar()
        self.Gender_var=StringVar()
        self.dob_var=StringVar()
        self.Phone_var=StringVar()
        self.Email_var=StringVar()


        #left frame

        left_frame=Frame(self.base,bd=5,relief=RIDGE,bg="RoyalBlue1")
        left_frame.place(x=20,y=80,width=350,height=600)

        Label(left_frame,text="Manage Students",bg="RoyalBlue1",fg="white",font=("Times",22,"bold")).grid(row=0,columnspan=2,pady=5)

        Label(left_frame,text="Roll No.",bg="RoyalBlue1",fg="white",font=("Times",16,"bold")).grid(row=1,column=0,pady=10,sticky="w")
        Entry(left_frame,textvariable=self.Rollno_var, font=("Times",14,"bold"),bd=5).grid(row=1,column=1,pady=10,sticky="w")

        Label(left_frame,text="Name",bg="RoyalBlue1",fg="white",font=("Times",16,"bold")).grid(row=2,column=0,pady=10,sticky="w")
        Entry(left_frame,textvariable=self.Name_var,font=("Times",14,"bold"),bd=5).grid(row=2,column=1,pady=10,sticky="w")

        Label(left_frame,text="Gender",bg="RoyalBlue1",fg="white",font=("Times",16,"bold")).grid(row=3,column=0,pady=10,sticky="w")
        combo_gen=ttk.Combobox(left_frame,textvariable=self.Gender_var,width=7,font=("Times",14,"bold"),state="readonly")
        combo_gen['values']=("Male","Female","Others")
        combo_gen.grid(row=3,column=1,pady=10,sticky="w")

        Label(left_frame,text="D.O.B.",bg="RoyalBlue1",fg="white",font=("Times",16,"bold")).grid(row=4,column=0,pady=10,sticky="w")
        Entry(left_frame,textvariable=self.dob_var,font=("Times",14,"bold"),bd=5).grid(row=4,column=1,pady=10,sticky="w")

        Label(left_frame,text="Phone No.",bg="RoyalBlue1",fg="white",font=("Times",16,"bold")).grid(row=5,column=0,pady=10,sticky="w")
        Entry(left_frame,textvariable=self.Phone_var,font=("Times",14,"bold"),bd=5).grid(row=5,column=1,pady=10,sticky="w")

        Label(left_frame,text="Email",bg="RoyalBlue1",fg="white",font=("Times",16,"bold")).grid(row=6,column=0,pady=10,sticky="w")
        Entry(left_frame,textvariable=self.Email_var,font=("Times",14,"bold"),bd=5).grid(row=6,column=1,pady=10,sticky="w")

        Label(left_frame,text="Address",bg="RoyalBlue1",fg="white",font=("Times",16,"bold")).grid(row=7,column=0,pady=10,sticky="w")
        self.txt_address=Text(left_frame,width=22,height=2,font=("Times",14),bd=5)
        self.txt_address.grid(row=7,column=1,pady=10,sticky="w")

        
        #button Frame

        button_frame=Frame(left_frame,bd=5,relief=RIDGE, bg="RoyalBlue2")
        button_frame.place(x=10,y=480,width=321)

        Button(button_frame,text="Add",width=8,command=self.add_stu).grid(row=0,column=0,padx=6,pady=10)
        Button(button_frame,text="Update",width=8,command=self.update_data).grid(row=0,column=1,padx=6,pady=10)
        Button(button_frame,text="Delete",width=8,command=self.delete_data).grid(row=0,column=2,padx=6,pady=10)
        Button(button_frame,text="Clear",width=8,command=self.clear).grid(row=0,column=3,padx=6,pady=10)


        #right frame

        right_frame=Frame(self.base,bd=5,relief=RIDGE,bg="RoyalBlue1")
        right_frame.place(x=390,y=80,width=785,height=600)


        #table frame

        table_frame=Frame(right_frame,bd=5,relief=RIDGE,bg="RoyalBlue1")
        table_frame.place(x=10,y=20,width=755,height=550)

        scroll_x=Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(table_frame,orient=VERTICAL)
        self.data_table=ttk.Treeview(table_frame,columns=("Rollno","Name","Gender","dob","Phone","Email","Address"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.data_table.xview)
        scroll_y.config(command=self.data_table.yview)

        self.data_table.heading("Rollno",text="Roll No.")
        self.data_table.heading("Name",text="Name")
        self.data_table.heading("Gender",text="Gender")
        self.data_table.heading("dob",text="D.O.B.")
        self.data_table.heading("Phone",text="Phone No.")
        self.data_table.heading("Email",text="Email")
        self.data_table.heading("Address",text="Address")

        self.data_table['show']='headings'

        self.data_table.column("Rollno",width=90)
        self.data_table.column("Name",width=170)
        self.data_table.column("Gender",width=50)
        self.data_table.column("dob",width=80)
        self.data_table.column("Phone",width=90)
        self.data_table.column("Email",width=150)
        self.data_table.column("Address",width=150)

        self.data_table.pack(fill=BOTH,expand=1)
        self.data_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()

    def add_stu(self):
        if self.Rollno_var.get()=="" or self.Name_var.get()=="":
            messagebox.showerror("Error","Fill all the sections")
        else:

            conc=pymysql.connect(host="localhost",user="root",password="",database="dh_bbk11")
            cur=conc.cursor()
            cur.execute("insert into students values(%s,%s,%s,%s,%s,%s,%s)",(self.Rollno_var.get(),
                                                                            self.Name_var.get(),
                                                                            self.Gender_var.get(),
                                                                            self.dob_var.get(),
                                                                            self.Phone_var.get(),
                                                                            self.Email_var.get(),
                                                                            self.txt_address.get('1.0',END)
                                                                            ))
            conc.commit()
            self.fetch_data()
            self.clear()
            conc.close()
            messagebox.showinfo("Success","Data has been recorded")
    
    def fetch_data(self):
        conc=pymysql.connect(host="localhost",user="root",password="",database="dh_bbk11")
        cur=conc.cursor()
        cur.execute("select * from students")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.data_table.delete(*self.data_table.get_children())
            for row in rows:
                self.data_table.insert('',END,values=row)
            conc.commit()
        conc.close()

    def clear(self):
        self.Rollno_var.set("")
        self.Name_var.set("")
        self.Gender_var.set("")
        self.dob_var.set("")
        self.Phone_var.set("")
        self.Email_var.set("")
        self.txt_address.delete('1.0',END)

    def get_cursor(self,eve):
        cursor_row=self.data_table.focus()
        contents=self.data_table.item(cursor_row)
        row=contents['values']
        self.Rollno_var.set(row[0])
        self.Name_var.set(row[1])
        self.Gender_var.set(row[2])
        self.dob_var.set(row[3])
        self.Phone_var.set(row[4])
        self.Email_var.set(row[5])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[6])

    def update_data(self):
        conc=pymysql.connect(host="localhost",user="root",password="",database="dh_bbk11")
        cur=conc.cursor()
        cur.execute("update students set Name=%s,Gender=%s,dob=%s,Phone=%s,Email=%s,Address=%s where Rollno=%s",(
                                                                            self.Name_var.get(),
                                                                            self.Gender_var.get(),
                                                                            self.dob_var.get(),
                                                                            self.Phone_var.get(),
                                                                            self.Email_var.get(),
                                                                            self.txt_address.get('1.0',END),
                                                                            self.Rollno_var.get()
                                                                            ))
        conc.commit()
        self.fetch_data()
        self.clear()
        conc.close()

     
    def delete_data(self):
        conc=pymysql.connect(host="localhost",user="root",password="",database="dh_bbk11")
        cur=conc.cursor()
        cur.execute("delete from students where Rollno=%s",self.Rollno_var.get())
        conc.commit()
        conc.close()
        self.fetch_data()
        self.clear()

         
base=Tk()
stu=student(base)
base.mainloop()
