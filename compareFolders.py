print("正在启动...",end="")
import os,tempfile,copy,ctypes,sys
import tkinter.filedialog
from PIL import ImageFont
font = ImageFont.truetype("C:\\Windows\\Fonts\\simsun.ttc",16)
rootPath1=""
rootPath2=""
toolsPackageName1=""
toolsPackageName2=""
screenOut=[]
file1=1
file2=1
os.system("echo off")
fileName1="ghmToolsUpgrade1.tmp"
fileName2="ghmToolsUpgrade2.tmp"
nameStartAddress=-1
toolsPackageName1=""
toolsPackageName2=""
tempdir=tempfile.gettempdir()+"\\"
screenOut.append("正在启动...")
differt=[]#[0,1/2,filename,"none"] or [1,1/2,pathname,"none"]
class CmdColor:
    def __init__(self):
        self.FOREGROUND_DARKBLUE = 0x01 # 暗蓝色
        self.FOREGROUND_DARKGREEN = 0x02 # 暗绿色
        self.FOREGROUND_DARKSKYBLUE = 0x03 # 暗天蓝色
        self.FOREGROUND_DARKRED = 0x04 # 暗红色
        self.FOREGROUND_DARKPINK = 0x05 # 暗粉红色
        self.FOREGROUND_DARKYELLOW = 0x06 # 暗黄色
        self.FOREGROUND_DARKWHITE = 0x07 # 暗白色
        self.FOREGROUND_DARKGRAY = 0x08 # 暗灰色
        self.FOREGROUND_BLUE = 0x09 # 蓝色
        self.FOREGROUND_GREEN = 0x0a # 绿色
        self.FOREGROUND_SKYBLUE = 0x0b # 天蓝色
        self.FOREGROUND_RED = 0x0c # 红色
        self.FOREGROUND_PINK = 0x0d # 粉红色
        self.FOREGROUND_YELLOW = 0x0e # 黄色
        self.FOREGROUND_WHITE = 0x0f # 白色
        self.STD_INPUT_HANDLE = -10
        self.STD_OUTPUT_HANDLE= -11
        self.STD_ERROR_HANDLE = -12
        self.std_out_handle=ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
    def setCmdTextColor(self,color,handle=None):
        if handle==None:
            handle=self.std_out_handle
        Bool=ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool
    def reSetCmdColor(self):
        self.setCmdTextColor(self.FOREGROUND_DARKWHITE)
    def printWithColor(self,color,message):
        self.setCmdTextColor(color)
        print(message,end="")
        self.reSetCmdColor()
cmdcolor=CmdColor()
class MyErrow(Exception):
    pass
class DirNorFoundErorr(MyErrow):
    def __init__(self,s):
        self.s=s
    def __str__(self):
        return self.s
class NameMaxLenthErorr(MyErrow):
    def __init__(self):
        pass
    def __str__(self):
        return "名字长度错误"
def reSetScreen(add=None):
    global screenOut
    if add!=None:
        screenOut.append(copy.deepcopy(add))
    os.system("cls")
    for i in screenOut:
        print(i)
if True:
    screenOut[-1]=screenOut[-1][:-3]+"[done]"
    reSetScreen("正在获取文件夹名...")
    print("请选择第一个文件夹")
    toolsPackageName1=tkinter.filedialog.askdirectory(mustexist=True)
    #toolsPackageName1="E:/视频剪映"
    if toolsPackageName1=="":
        raise DirNorFoundErorr("目录缺失")
    print("请选择第二个文件夹")
    toolsPackageName2=tkinter.filedialog.askdirectory(mustexist=True)
    #toolsPackageName2="C:/Users/21638/Desktop/视频剪映"
    toolsPackageName1+="/"
    toolsPackageName2+="/"
    if toolsPackageName2=="":
        raise DirNorFoundErorr("目录缺失")
    screenOut[-1]=screenOut[-1][:-3]+"[done]"
    screenOut.append("    目录1:"+toolsPackageName1)
    screenOut.append("    目录2:"+toolsPackageName2)
    reSetScreen("正在分析文件目录...")

    screenOut[-1]=screenOut[-1][:-3]+"[done]"
    reSetScreen("正在分析对比目录...")
    different=[]
    Filelist=[{},{}]

    def dfsList(now):
        retsult={"name":copy.copy(now),"files":[],"folders":[],"sonList":{}}
        nowAll=os.listdir(now)
        for i in nowAll:
            if os.path.isdir(now+i):
                retsult["folders"].append(copy.copy(i))
                retsult["sonList"][i]=dfsList(now+i+"/")
            else:
                retsult["files"].append(copy.copy(i))
        return retsult
    
    def dfsFind(now1,now2,dir):
        global different
        
        for i in now1["files"]:
            if i not in now2["files"]:
                different.append([0,0,dir+i,"None"])
        for i in now2["files"]:
            if i not in now1["files"]:
                different.append([0,1,dir+i,"None"])
        sonList=[]
        for i in now1["folders"]:
            if i in now2["folders"]:
                sonList.append(copy.copy(i))
            else:
                different.append([1,0,dir+i,"None"])
        for i in now2["folders"]:
            if i not in now1["folders"]:
                different.append([1,1,dir+i,"None"])
        for i in sonList:
            dfsFind(now1["sonList"][i],now2["sonList"][i],dir+i+"/")
    def load():
        Filelist=[dfsList(toolsPackageName1),dfsList(toolsPackageName2)]
        dfsFind(Filelist[0],Filelist[1],"/")
    load()
    print(different)
    
    showClass=["None","Copy","Delete","Copied","Deleted","Errow"]
    show={"None":[],"Copy":[],"Copied":[],"Delete":[],"Deleted":[],"Errow":[]}
    showColor={"None":cmdcolor.FOREGROUND_GREEN,"Copy":cmdcolor.FOREGROUND_WHITE,"Copied":cmdcolor.FOREGROUND_PINK,"Delete":cmdcolor.FOREGROUND_RED,"Deleted":cmdcolor.FOREGROUND_YELLOW,"Errow":cmdcolor.FOREGROUND_DARKRED}
    showTitle=ttle={"None":"========None========","Copy":"========Copy========","Copied":"=======Copied=======","Delete":"=======Delete=======","Deleted":"=======Deleted======","Errow":"=======Errow========"}
    showAdd=["目录1","目录2"]
    showType=["File   ","Folder "]
    rootPathMap=[copy.deepcopy(toolsPackageName1),copy.deepcopy(toolsPackageName2)]
    while True:
        le=font.getlength(showAdd[0])
        if le==48:
            break
        elif le>48:
            showAdd[0]=showAdd[0][1:]
        else:
            showAdd[0]+=" "
    while True:
        le=font.getlength(showAdd[1])
        if le==48:
            break
        elif le>48:
            showAdd[1]=showAdd[1][1:]
        else:
            showAdd[1]+=" "
    showAdd[0]+="   "
    showAdd[1]+="   "
    sum=0
    maxNameLength=496
    for i in different:
        width=font.getlength(i[2])
        name=i[2]
        maxNameLength=max(maxNameLength,font.getlength(name))
    for i in different:
        width=font.getlength(i[2])
        name=i[2]
        while True:
            le=font.getlength(name)
            if le==maxNameLength:
                break
            elif le>maxNameLength:
                raise 
            else:
                name+=" "
        name+="  "
        show["None"].append([copy.copy(sum),name,showType[i[0]],showAdd[i[1]],i[3],False,i[2],i[1]])
        sum+=1
    header="-NO-|"+"-"*int((maxNameLength/8-3)//2)+"NAME"+"-"*int((maxNameLength/8-2)//2)+"|-TYPE-|ROOTPATH|--WAY-----\n"
    universalSet=set(range(len(show["None"])))

    def difList():
        global show,showClass,showTitle,showColor,header,cmdcolor
        #os.system("cls")
        #cmdcolor.printWithColor(cmdcolor.FOREGROUND_GREEN,str(i[0]).ljust(5)+i[1]+i[2]+i[3]+i[4]+"\n")
        for i in showClass:
            cmdcolor.printWithColor(cmdcolor.FOREGROUND_BLUE,showTitle[i]+"\n")
            if len(show[i])==0:
                cmdcolor.printWithColor(showColor[i],"EMPTY\n")
                continue
            cmdcolor.printWithColor(showColor[i],header)
            for j in show[i]:
                cmdcolor.printWithColor(showColor[i],str(j[0]).ljust(5)+j[1]+j[2]+j[3]+j[4]+"\n")




    
    errSum=0
    result=""

    def findName(s):
        print("findName: "+s)
        s=s.replace("/","\\")
        print("findNameReplace"+s)
        global showClass,showColor
        result=set()
        if s[0]!="\\":
            s="\\"+s
        print("findNameReplace"+s)
        for i in showClass:
            for j in show[i]:
                if j[6]==s:
                    result.add(j[0])
        return result
    def findType(s):
        print("findType: "+s)
        if s.lower()=="folder":
            s="folder "
        if s.lower()=="file":
            s="File   "
        global showClass,showColor
        result=set()
        for i in showClass:
            for j in show[i]:
                if j[2].lower()==s.lower():
                    result.add(j[0])
        return result
    def findRootPath(s):
        print("findRootPath: "+s)
        global showClass,showColor
        s=s.replace("/","\\")
        print("findRootPathReplace"+s)
        result=set()
        for i in showClass:
            for j in show[i]:
                if rootPathMap[j[7]]==s:
                    result.add(j[0])
        return result
    def findWay(s):
        print("findWay: "+s)
        result=set()
        if s not in show:
            return set()
        for i in show[s]:
            result.add(i[0])
        return result
    def doCommand(command):
        print("DOCOMMAND START")
        global errSum,result
        if len(command)==0:
            errSum+=1
            return "空的指令"
        while command[0]==" ":
            command=command[1:]
        if command.find(" ")==-1:
            title=command
            chooser=""
        else:
            title=command[:command.find(" ")]
            chooser=command[command.find(" ")+1:]
        if title.lower() == "cls":
            result=""
            return ""
        if title.lower() == "help":
            errSum=0
            return """帮助:
命令格式:命令 选择器
命令有如下几种(不分大小写):
copy:将符合选择器的项目移入Copy
none:将符合选择器的项目移入None
delete:将符合选择器的项目移入Delete
*以上三个命令不会对[Copyed,Deleted,Errow]中的项目进行操作
help:显示此帮助菜单
exit 退出程序
choo:仅展示选择器结果，不进行操作
execute:按每个项目的类别进行操作
cls:清屏
选择器(区分大小写):
选择器本质是一个集合，以{}包括
# 有如下特殊定义(以#开头全部大写):
    # ALL:全集
    # NAME("s"):名字是s的项目组成的集合
    #TYPE("s"):种类是s的项目组成的集合
    # #ROOTPATH("s"):根目录是s的项目组成的集合
    # #WAY("s"):处理方式是s的项目组成的集合
# 集合的运算:
    A交B A&B
    A并B A|B
    B关于A的补集 A^B
# 示例:
    1. {0,1,2,3}编号为1、2、3的项目
    2. #NAME("\\py3.8\\") 名字为\py3.8\的项目
    3. #ALL^#NAME("\\py3.8\\")  名字不是\py3.8\的项目"""
        if title.lower() == "execute":
            while True:
                print("将要复制"+str(len(show["Copy"]))+"个项目，\n并删除"+str(len(show["Delete"]))+"个项目?(Y/n)",end="")
                sure=input()
                if sure.lower()=="y":
                    break
                if sure.lower()=="n":
                    errSum=0
                    return "命令已取消"
            for i in show["Copy"]:
                exe=""
                if i[2]=="File   ":
                    exe="copy \""+rootPathMap[int(i[7])].replace("/","\\")+i[6][1:].replace("/","\\")+"\" \""+rootPathMap[1-i[7]].replace("/","\\")+i[6][1:].replace("/","\\")+"\" /V /Y"
                else:
                    exe="xcopy \""+rootPathMap[i[7]].replace("/","\\")+i[6][1:].replace("/","\\")+"\" \""+rootPathMap[1-i[7]].replace("/","\\")+i[6][1:].replace("/","\\")+"\\\" /E"
                print(exe)
                os.system(exe)

            for i in show["Delete"]:
                exe=""
                if i[2]=="File   ":
                    exe="del \""+rootPathMap[i[7]].replace("/","\\")+i[6][1:].replace("/","\\")+"\" /Q"
                else:
                    exe="rd \""+rootPathMap[i[7]].replace("/","\\")+i[6][1:].replace("/","\\")+"\" /S /Q"
                print(exe)
                os.system(exe)
            while len(show["Copy"])>0:
                show["Copied"].append(copy.deepcopy(show["Copy"][0]))
                show["Copied"][-1][4]="Copied"
                del show["Copy"][0]
            while len(show["Delete"])>0:
                show["Deleted"].append(copy.deepcopy(show["Delete"][0]))
                show["Deleted"][-1][4]="Deleted"
                del show["Delete"][0]
            errSum=0
            return "完成"
        if title.lower()=="exit":
            while True:
                print("不对当前文件做更改并退出?(Y/n)",end="")
                sure=input()
                if sure.lower()=="n":
                    errSum=0
                    return "取消退出"
                if sure.lower()=="y":
                    sys.exit()
        elif len(chooser)==0 or command.find(" ")==-1:
            errSum+=1
            return "没有选择器"
        while chooser[0]==" ":
            chooser=chooser[1:]
            if chooser=="":
                errSum+=1
                return "ERROW:No chooser"
        chooser=chooser.replace("\\","\\\\").replace("#ALL","universalSet").replace("#NAME","findName").replace("#TYPE","findType").replace("#ROOTPATH","findRootPath").replace("#WAY","findWay")
        #chooser=chooser[:-1]
        print("replace:"+chooser)
        try :
            chooser=eval(chooser)
        except BaseException as err:
            errSum+=1
            print("ERROW IN COMMAND: " + str(err))
            return str(err)
        print("eval:",chooser)
        if title.lower()=="copy":
            num=0
            for i in ["None", "Copy", "Delete"]:
                if i=="Copy":
                    continue
                j=0
                while j<len(show[i]):
                    if show[i][j][0] in chooser:
                        num+=1
                        show["Copy"].append(copy.deepcopy(show[i][j]))
                        show["Copy"][-1][4]="Copy"
                        del show[i][j]
                    else:
                        j+=1
            errSum=0
            return "已将"+str(num)+"个项目移入Copy"
        if title.lower()=="delete":
            num=0
            for i in ["None", "Copy", "Delete"]:
                if i=="Delete":
                    continue
                j=0
                while j<len(show[i]):
                    if show[i][j][0] in chooser:
                        num+=1
                        show["Delete"].append(copy.deepcopy(show[i][j]))
                        show["Delete"][-1][4]="Delete"
                        del show[i][j]
                    else:
                        j+=1
            errSum=0
            return "已将"+str(num)+"个项目移入Delete"
        if title.lower()=="none":
            num=0
            for i in ["None", "Copy", "Delete"]:
                if i=="None":
                    continue
                j=0
                while j<len(show[i]):
                    if show[i][j][0] in chooser:
                        num+=1
                        show["None"].append(copy.deepcopy(show[i][j]))
                        show["None"][-1][4]="None"
                        del show[i][j]
                    else:
                        j+=1
            errSum=0
            return "已将"+str(num)+"个项目移入None"
        if title.lower()=="choo":
            return "所指定的选择器:"+str(chooser)
        errSum+=1
        return "未知的命令:"+title
        
    while True:
        difList()
        print("\n"+result)
        if errSum>=3:
            print("\n键入\"help\"以查看帮助")
        command=input("COMMAND>")
        res=doCommand(command)
        result+=">"+command+"\n"+res+"\n"


# except BaseException as err:
#     print(str(err.__class__.__name__)+":  "+str(err))
#     screenOut.append(str(err.__class__.__name__)+"\n"+str(err))
# finally:
#     time.sleep(0.5)
#     #reSetScreen()
#     os.system("pause")