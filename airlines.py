import tkinter as tk
from tkinter import ttk,messagebox
import pymysql

class airline():
    def __init__(self, root):
        self.root = root
        self.root.title("Airlines Management")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Airlines Management System", bd=4, relief="groove",fg="light green", bg=self.clr(120,40,100), font=("Arial",50,"bold"))
        title.pack(side="top",fill="x")

        # info Frame

        infoFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(100,150,130))
        infoFrame.place(width=self.width/3, height=self.height-180, x=30, y=100)

        flightLbl = tk.Label(infoFrame,text="Flight_No:", bg=self.clr(100,150,130),fg="white", font=("Arial",15,"bold"))
        flightLbl.grid(row=0, column=0, padx=20, pady=30)
        self.fNoIn = tk.Entry(infoFrame, width=20, font=("Arial",15,"bold"),bd=2)
        self.fNoIn.grid(row=0, column=1, padx=10, pady=30)

        idLbl = tk.Label(infoFrame,text="ID_No:", bg=self.clr(100,150,130),fg="white", font=("Arial",15,"bold"))
        idLbl.grid(row=1, column=0, padx=20, pady=30)
        self.idIn = tk.Entry(infoFrame, width=20, font=("Arial",15,"bold"),bd=2)
        self.idIn.grid(row=1, column=1, padx=10, pady=30)

        nameLbl = tk.Label(infoFrame,text="Name:", bg=self.clr(100,150,130),fg="white", font=("Arial",15,"bold"))
        nameLbl.grid(row=2, column=0, padx=20, pady=30)
        self.nameIn = tk.Entry(infoFrame, width=20, font=("Arial",15,"bold"),bd=2)
        self.nameIn.grid(row=2, column=1, padx=10, pady=30)

        resBtn = tk.Button(infoFrame,command=self.resFun, text="Reserve Seat", width=20, bd=3,relief="raised",font=("Arial",20,"bold"))
        resBtn.grid(row=3, column=0, padx=30, pady=40, columnspan=2)

        passengerBtn = tk.Button(infoFrame,command=self.passengerFun, text="Passenger's Details", width=20, bd=3,relief="raised",font=("Arial",20,"bold"))
        passengerBtn.grid(row=4, column=0, padx=30, pady=30, columnspan=2)

        # detail Frame

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge",bg=self.clr(150,180,100))
        self.detFrame.place(width=self.width/2+110, height=self.height-180, x=self.width/3+60, y=100)
        
        self.showFlights()

    def tabFun(self):

        self.lbl1 = tk.Label(self.detFrame, text="Flight Details", bd=3,relief="flat", bg=self.clr(120,180,200),font=("Arial",25,"bold"))
        self.lbl1.pack(side="top", fill="x")

        self.tabFrame1 = tk.Frame(self.detFrame, bd=4, relief="sunken")
        self.tabFrame1.place(width=self.width/2+70, height=self.height-270, x=17,y=65)

        x_scrol = tk.Scrollbar(self.tabFrame1, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(self.tabFrame1, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table1 =ttk.Treeview(self.tabFrame1,xscrollcommand=x_scrol.set,yscrollcommand=y_scrol.set,
                                  columns=("fNo","dep","des","seats","price"))
        
        x_scrol.config(command=self.table1.xview)
        y_scrol.config(command=self.table1.yview)
        
        
        self.table1.heading("fNo", text="FlightNo")
        self.table1.heading("dep", text="Departure")
        self.table1.heading("des", text="Destination")
        self.table1.heading("seats", text="Seats")
        self.table1.heading("price", text="Price")
        self.table1["show"]="headings"

        self.table1.column("fNo", width=100)
        self.table1.column("dep",width=100)
        self.table1.column("des", width=150)
        self.table1.column("seats", width=100)
        self.table1.column("price", width=120)
        
        self.table1.pack(fill="both", expand=1)

    def passengerFun(self):
        try:
            self.dbFun()
            self.cur.execute("select * from passenger")
            rows = self.cur.fetchall()
            self.tabFun2()
            self.table2.delete(*self.table2.get_children())
            for j in rows:
                self.table2.insert('',tk.END,values=j)
            
            self.con.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def tabFun2(self):
       
        self.lbl1.destroy()
        self.tabFrame1.destroy() 

        self.lbl2 = tk.Label(self.detFrame, text="Passenger's Details", bd=3,relief="flat", bg=self.clr(120,180,200),font=("Arial",25,"bold"))
        self.lbl2.pack(side="top", fill="x")

        self.tabFrame2 = tk.Frame(self.detFrame, bd=4, relief="sunken")
        self.tabFrame2.place(width=self.width/2+70, height=self.height-270, x=17,y=65)

        x_scrol = tk.Scrollbar(self.tabFrame2, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(self.tabFrame2, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table2 =ttk.Treeview(self.tabFrame2,xscrollcommand=x_scrol.set,yscrollcommand=y_scrol.set,
                                  columns=("id","name","fNo"))
        
        x_scrol.config(command=self.table2.xview)
        y_scrol.config(command=self.table2.yview)
        
        
        self.table2.heading("id", text="Passenger_Id")
        self.table2.heading("name", text="Passenger_Name")
        self.table2.heading("fNo", text="Flight_No")
        self.table2["show"]="headings"

        self.table2.column("id", width=100)
        self.table2.column("name",width=150)
        self.table2.column("fNo", width=100)
        
        self.table2.pack(fill="both", expand=1)    

    def resFun(self):
        f = self.fNoIn.get()
        id = self.idIn.get()
        name = self.nameIn.get()

        if f and id and name:
            fNo = int(f)            
            try:

                self.lbl2.destroy()
                self.tabFrame2.destroy()
                self.dbFun()
                
                self.cur.execute("select dep,des,seats,price from flight where flightNo=%s",fNo)
                row = self.cur.fetchone()
                depVar = row[0]
                desVar = row[1]
                seatVar = row[2]
                priceVar= row[3]
                if seatVar >0:
                    self.cur.execute("insert into passenger(id,name,flightNo) values(%s,%s,%s)",(id,name,fNo))
                    self.con.commit()
                    updSeat = seatVar-1
                    self.cur.execute("update flight set seats=%s where flightNo=%s",(updSeat,fNo))
                    self.con.commit()
                    tk.messagebox.showinfo("Success",f"Seat is reserved in flight_No.{fNo} from {depVar} to {desVar}\nOnly in {priceVar}.Rs for Mr/Mrs.{name}")
                    self.cur.execute("select * from flight where flightNo=%s",fNo)
                    data = self.cur.fetchone()
                    self.tabFun()
                    self.table1.delete(*self.table1.get_children())
                    self.table1.insert('',tk.END,values=data)

                    self.con.close()
                else:
                    tk.messagebox.showerror("Sorry",f"All seats Reserved in flight_No.{fNo}")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
        else:
            tk.messagebox.showerror("Error","Fill All Input Fields!")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()
    
    def showFlights(self):
        try:
            self.dbFun()
            self.cur.execute("select * from flight")
            data = self.cur.fetchall()
            self.tabFun()
            self.table1.delete(*self.table1.get_children())

            for i in data:
                self.table1.insert('',tk.END,values=i)

            self.con.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

root = tk.Tk()
obj = airline(root)
root.mainloop()