import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askdirectory
import os
from PIL import Image,ImageTk
import shutil
import sys

class Model:
    def __init__(self,localdata):
        self.localdata=localdata
    
    @property
    def localdata(self):
        return self.__localdata
    
    @localdata.setter
    def localdata(self,value):
        """
        Validate the email
        :param value:
        :return:
        """
       
        self.__localdata = value
        
    
    
class View(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
         # set the controller
        self.controller = None
        self.arr=[]
        self.nodes = dict()
        self.sortlength=0
        self.subfolder=0
        self.outputfile=[]
        self.localpath= os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, 'frozen', False):
        # 如果在執行的是獨立應用程式（.app），獲取 .app 根目錄的路徑
            self.localpath=os.path.dirname(sys.executable)
        self.folder_image = Image.open(self.localpath+"/Folder.png")
        self.file_image = Image.open(self.localpath+"/file.png")
        self.folder_image=self.folder_image.resize((20,20),Image.Resampling.LANCZOS)
        self.file_image=self.file_image.resize((15,15),Image.Resampling.LANCZOS)
        self.folder_image= ImageTk.PhotoImage(self.folder_image)
        self.file_image= ImageTk.PhotoImage(self.file_image)

        #選擇檔案位置
        self.L1 = ttk.Label(self, text='選擇檔案位置:')
        self.L1.grid(row=0, column=0,sticky='w')
        self.folder_entry=ttk.Entry(self,width=30)
        self.folder_entry.grid(row=1,column=0,sticky=tk.NSEW,pady=5)

        # 所抓取的資料夾名稱長度 #Label
        self.L2 = ttk.Label(self, text='所抓取的資料夾名稱長度:')
        self.L2.grid(row=2, column=0,sticky='w')
        # self.filelong_entry=ttk.Entry(self,width=30)
        # self.filelong_entry.grid(row=3,column=0,sticky=tk.NSEW,pady=5)
        self.filelong_entry=ttk.Combobox(self,textvariable=tk.StringVar)
        self.filelong_entry.grid(row=3,column=0,sticky=tk.NSEW,pady=5)
        self.filelong_entry['value']=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
        self.filelong_entry.current(9)
        #抓取的關鍵字
        self.L3 = ttk.Label(self, text='抓取的關鍵字:')
        self.L3.grid(row=4, column=0,sticky='w')
        self.keyword_entry=ttk.Entry(self,width=30,text="NULL")
        self.keyword_entry.insert(0,"NULL")
        self.keyword_entry.grid(row=5,column=0,sticky=tk.NSEW,pady=5)

        #時間範圍
        self.pw1=ttk.LabelFrame(self,text="時間範圍")
        self.pw1.grid(row=6,column=0,sticky='w')
        
        #開始時間
        self.L4=ttk.Label(self.pw1,text="開始時間")
        self.L4.grid(row=0,column=0,sticky='w')
        self.calstart=DateEntry(self.pw1,selectmode ='day',width=20)
        self.calstart.grid(row=1,column=0,pady=50)
        self.calstart_hour=ttk.Combobox(self.pw1,textvariable=tk.StringVar)
        self.calstart_hour['value']=self.arr
        self.calstart_hour.grid(row=1,column=1)

        #結束時間
        self.L4=ttk.Label(self.pw1,text="結束時間")
        self.L4.grid(row=2,column=0,sticky='w')
        self.calend=DateEntry(self.pw1,selectmode = 'day',data_pattern='yyyy-mm-dd',width=20)
        self.calend.grid(row=3,column=0,pady=50)
        self.calend_hour=ttk.Combobox(self.pw1,textvariable=tk.StringVar)
        self.calend_hour['value']=self.arr
        self.calend_hour.grid(row=3,column=1)

        #搜索開始
        self.btn_sort=ttk.Button(self.pw1,text="搜索",command=self.sortfile)
        self.btn_sort["state"]="disable"
        self.btn_sort.grid(row=4,column=0,sticky='w')
        

        #列出所有的檔案名稱
        self.L5=ttk.Label(self,text="列出所有的檔案名稱",width=40)
        self.L5.grid(row=0,column=1,sticky='w',padx=50)
        self.foldertreeviewer=ttk.Treeview(self)
        self.foldertreeviewer.grid(row=1,rowspan=7,column=1,pady=50,padx=50,sticky=tk.NSEW)

        #匯出檔案
        self.L6=ttk.Label(self,text="匯出檔案")
        self.L6.grid(row=0,column=2,sticky='w',padx=30)
        self.btn_export=ttk.Button(self,command=self.outfilebtn)
        self.btn_export.grid(row=1,column=2,padx=30)

        #設定Menu
        menubar=Menu(parent)
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(label="打開資料夾",command=self.chooseFolder)
        filemenu.add_command(label="開啟舊檔案",command=self.chooseoldFolder)
        # filemenu.add_separator()
        filemenu.add_command(label="匯出")
        menubar.add_cascade(label="開始", menu=filemenu)#为filemenu命名为‘文件’
        parent.config(menu=menubar) 
        # self.myMenu=Menu(self)
        # self.myMenu.add_command(label="WWW")
        # self.config(menu=self.myMenu)
        

        
        #設定
    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
        self.arr=self.controller.get_hour_array()
        self.calstart_hour['value']=self.arr
        self.calend_hour['value']=self.arr
        self.calstart_hour.current(0)
        self.calend_hour.current(0)

    def chooseFolder(self):
        choosename=askdirectory()
        if choosename=='': return
        self.folder_entry.delete(0,tk.END)
        self.folder_entry.insert(0,choosename)
        #add claer
        for item in self.foldertreeviewer.get_children():
            self.foldertreeviewer.delete(item)
        self.btn_sort["state"]="normal"
        self.foldertreeviewer.heading('#0',text="Foldername")
        self.insert_node('', choosename, choosename)
        self.foldertreeviewer.bind('<<TreeviewOpen>>', self.open_node)
        

    def chooseoldFolder(self):
        choosename=askdirectory(initialdir='')
        if choosename=='': return
        self.folder_entry.delete(0,tk.END)
        self.folder_entry.insert(0,choosename)
        #add claer
        for item in self.foldertreeviewer.get_children():
            self.foldertreeviewer.delete(item)
        self.btn_sort["state"]="normal"
        self.foldertreeviewer.heading('#0',text="Foldername")
        self.insert_node('', choosename, choosename)
        self.foldertreeviewer.bind('<<TreeviewOpen>>', self.open_node)
      
    def insert_node(self, parent, text, path):
        abspath=os.path.abspath(path)
        if os.path.isdir(abspath):
            node = self.foldertreeviewer.insert(parent, 'end', text=text, open=False,image=self.folder_image)
            self.nodes[node] = abspath
            self.foldertreeviewer.insert(node, 'end')
        else:
            node = self.foldertreeviewer.insert(parent, 'end', text=text, open=False,image=self.file_image)
            
    def open_node(self, event):
        node = self.foldertreeviewer.focus()
        print(self.nodes)
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.foldertreeviewer.delete(self.foldertreeviewer.get_children(node))
            self.subfolder+=1
            self.outputfile.clear()
            for p in os.listdir(abspath):
                if len(p)==self.sortlength or self.sortlength==0 or self.subfolder!=1 :
                    print("p is"+p)
                    #在寫一個找關鍵字的函式
                    print(abspath+"/"+p)
                    print(p,self.keyword_entry.get())
                    if len(p)==self.sortlength and self.search_keyword_in_directory(abspath+"/"+p,self.keyword_entry.get()):
                        self.insert_node(node, p, os.path.join(abspath, p))
                        self.outputfile.append(abspath+"/"+p)
                    elif len(p)!=self.sortlength:
                        self.insert_node(node, p, os.path.join(abspath, p))

                    if (p.find(".txt")!=-1 or p.find(".log")!=-1):
                        print(self.sort_keyword(abspath+"/"+p,self.keyword_entry.get()))                
            print(self.subfolder)

    
    def sortfile(self):
        self.subfolder=0
        self.sortlength=int(self.filelong_entry.get())
        for item in self.foldertreeviewer.get_children():
            self.foldertreeviewer.delete(item)
        self.foldertreeviewer.heading('#0',text="Foldername")
        self.insert_node('', self.folder_entry.get(), self.folder_entry.get())
        self.foldertreeviewer.bind('<<TreeviewOpen>>', self.open_node)

    def sort_keyword(self,txtfile,keyword):
        with open(txtfile,"r",encoding="utf-8") as f:
            data=f.read()
        chinese_dot_list=data.split('。')
        match_list = []
        for sentence in chinese_dot_list:
            if "Teardown-3-1" in sentence:
                return True
        return False
    
    def search_keyword_in_directory(seld,mypath, keyword):
    # 存储匹配的文件路径
        matching_files = []

        # 递归遍历文件夹
        for root, dirs, files in os.walk(mypath):
            for file in files:
                if ".log" in file or ".txt" in file or ".csv" in file:
                    file_path = os.path.join(root, file)
                    try:
                        # 尝试打开文件并搜索关键字
                        with open(file_path, 'r', encoding='utf-8',errors='ignore') as f:
                            content = f.read()
                            if keyword in content:
                                print("has key word"+file_path)
                                return True
                    except Exception as e:
                        # 处理文件打开错误等异常
                        print(f"Error processing {file_path}: {str(e)}")

        return False
    
    def outfilebtn(self):
        if self.outputfile:
           choosefolder=askdirectory(initialdir='')
           for folders in self.outputfile:
            floder=os.path.basename(folders)
            shutil.copytree(folders,choosefolder+"/"+floder)
    
 





class Controller:
    def __init__(self,model,view):
        self.model=model
        self.view=view
        self.arr=[]
        for i in range(24):
            if i<10:
                self.arr.append('0'+str(i)+':00:00')
            else:
                self.arr.append(str(i)+':00:00')

    def get_hour_array(self):
        return self.arr

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tkinter MVC Demo')

        #create a model
        model=Model('CaptureSN')

        #create Menu
        # menubar=Menu(self)
        # filemenu = Menu(menubar, tearoff=False)
        # filemenu.add_command(label="打開文件")
        # filemenu.add_command(label="開啟舊檔案")
        # # filemenu.add_separator()
        # filemenu.add_command(label="匯出")
        # menubar.add_cascade(label="開始", menu=filemenu)#为filemenu命名为‘文件’
        # self.config(menu=menubar) 

        #create a view and place it on the root window
        view=View(self)
        view.grid(row=0,column=0,padx=10,pady=10)

        #create a controller
        controller=Controller(model,view)

        # set the controller to view
        view.set_controller(controller)


#Call Main
if __name__=='__main__':
    app=App()
    app.mainloop()



