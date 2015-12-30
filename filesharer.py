import os
from tkinter import *
from tkinter.filedialog import *
from socket import *
from os import *
import sys
from threading import Thread               
                
class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("A simple GUI")
        self.n=0
        self.geometry("550x500+200+200")
        self.label1=Label(self,text="A naive app to share files",font=22,bg='yellow').grid(row=0,column=1,padx=20,pady=20,sticky=NW)
        self.close_button = Button(self, text="Close", command=self.destroy)
        self.close_button.grid(row=0,column=3)
        self.l1 = Label(self, text="IP Address of server computer::").grid(row=1,column=0,padx=20)
        self.e1=Entry(self)
        self.e1.insert(0,"127.0.0.1")
        self.e1.grid(row=1,column=1)
        
        self.l2 = Label(self,text="Port::").grid(row=2,padx=20)
        self.e2=Entry(self)
        self.e2.insert(0,"5000")
        self.e2.grid(row=2,column=1,pady=15)
       
        self.button1=Button(self,text="send",command=self.send).grid(row=3,column=0,pady=20)

        self.button2=Button(self,text="Recieve",command=self.recieve).grid(row=3,column=1,pady=20)
        self.T=Text(self,width=70,height=10,state=NORMAL)
        self.T.grid(row=10,columnspan=6,pady=30)
        self.T.insert(END,"Progress bar\n")
        
        #self.redir=RedirectText(self.T)
        
     
        
    def recieve(self):
        if self.n==0:
                self.e3=Entry(self,width=25)
                self.e3.insert(0,os.getcwd())
                self.e3.grid(row=4,column=0,padx=10,pady=15)
                self.b3=Button(self,text="Browse",command=self.browse_rec).grid(row=4,column=1,pady=15)
                self.b5=Button(self,text="start!",command=self.threadclient).grid(row=5,column=1)
                self.n=1
        
    def send(self):
        if self.n==0:
                self.e4=Entry(self,width=20)
                self.e4.insert(0,os.getcwd())
                self.e4.grid(row=4,column=0,padx=10,pady=15)
                self.b4=Button(self,text="Browse",command=self.browse_send).grid(row=4,column=1,pady=15,padx=15)
                self.n=1
        
    def browse_rec(self):
        self.direc=askdirectory()
        print(self.direc)
        self.e3.delete(0,END)
        self.e3.insert(0,self.direc)
        
   
    def browse_send(self):
        path=askopenfilename()
        print(path)
        self.e4.delete(0,END)
        self.e4.insert(0,path)
        self.b5=Button(self,text="start!",command=self.serverthread).grid(row=5,column=1)
    
    def serverthread(self):
        self.Tr=Thread(target=self.server)
        self.Tr.start()

    def server(self):
        self.s=socket()
        self.host=self.e1.get()
        self.port=int(self.e2.get())
        self.s.bind((self.host,self.port))
        self.s.listen(5)
        
        print("server listening...")
        self.T.insert(END,"server listening...\n")
        while True:
                c,addr=self.s.accept()
                print('got connection from',addr)
                self.T.insert(END,'got connection from '+str(addr)+"\n")
                self.data=c.recv(1024)
                print("server recieved:: ",repr(self.data))
                self.T.insert(END,"server recieved:: "+repr(self.data)+"\n")
                self.filename=self.e4.get()
                c.send(self.filename.rpartition('/')[2].encode('utf8'))
                c.send(str(os.path.getsize(self.filename)).encode('utf8'))
                print(os.path.getsize(self.filename))
                f = open(self.filename,'rb')
                l = f.read(1024)
                while(l):
                        c.send(l)
                        l=f.read(1024)
                        
                f.close()        
                print('Done sending')
                self.T.insert(END,'Done sending\n')
                c.send(b'Thank you for connecting')
                self.T.insert(END,'Thank you for connecting\n')
                c.close()
                #sys.stdout=self.redir 
                break
                
    def threadclient(self):
        self.Tr=Thread(target=self.client)
        self.Tr.start()
        
    def client(self):
        self.s=socket()
        self.host=self.e1.get()
        self.port=int(self.e2.get())
        self.s.connect((self.host,self.port))
        self.s.send(b"Hello server!")
        os.chdir(self.e3.get())
        self.filename=self.s.recv(1024).decode("utf8")
        print(self.filename)
        self.filesize=int(self.s.recv(1024).decode('utf8'))
        print(self.filesize)
        self.filesize=int(self.filesize)
        totalrecv=0
        with open('new_'+self.filename,'wb') as f:
                print('file opened')
                self.T.insert(END,'file opened\n')
                while True:
                      
                        self.data=self.s.recv(1024)
                        totalrecv += len(self.data)
                        #print(totalrecv)
                        print("{0:.2f}".format((totalrecv/float(self.filesize))*100)+ "% Done")
                        #self.T.insert(END,"Recieving...\n")
                        if not self.data:
                                break   
                        f.write(self.data)
        f.close()
        print('Successfully got the file')
        self.T.insert(END,'Successfully got the file\n')
        self.s.close()
        print('connection closed')
        self.T.insert(END,'Connection closed\n')
        #sys.stdout=self.redir 
    
                                            
app=App()
app.mainloop()


