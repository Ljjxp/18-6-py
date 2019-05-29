import tkinter as tk
from tkinter import messagebox  
import pickle
import json as js
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
import tkinter.font as tkfont
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

import os

window = tk.Tk()
window.title('爬虫')
window.geometry('450x300')
ft = tkfont.Font(family='华文行楷', size=14)
ftt = tkfont.Font(family='华文行楷', size=10)
canvas = tk.Canvas(window,bg='#5d8fff' ,height=100, width=450)

canvas.pack(side='top')


tk.Label(window, text='用户名: ',font=ft).place(x=65, y= 150)
tk.Label(window, text='密码: ',font = ft).place(x=65, y= 190)
name = tk.StringVar()
name.set('')
entername = tk.Entry(window, textvariable=name)
entername.place(x=160, y=150)
password = tk.StringVar()
enterpassword = tk.Entry(window, textvariable=password, show='*')
enterpassword.place(x=160, y=190)

global jN_exp_dict
global jN_edu_dict
global jTy_size_dict
global jTy_size_np
global jTy_financ_dict
global jTy_financ_np
global jM_low_dict
global nd_jM_low

jNeed_exp = []
jNeed_edu = []
jTy_type = []
jTy_financ = []
jTy_size = []
jMoney = []
jM_low = []

def analysis():
    global jN_exp_dict
    global jN_edu_dict
    global jTy_size_dict
    global jTy_size_np
    global jTy_financ_dict
    global jTy_financ_np
    global jM_low_dict
    global nd_jM_low
    def line_num(File):
#判断文件行数的函数
        f=open(File,'r', encoding='UTF-8-sig')
        lines=f.readlines()
        f.close()
        n=0
        for line in lines:
            n=n+1
        return n-1
    
    def findSprit(Str):
    #单个‘/’or'k'判断
        for i in range(len(Str)):
            if Str[i] == '/' or Str[i] == 'k' or Str[i] == 'K':
                return i
            
    def findDobSprit(Str):
    #两个‘/’判断
        j = []
        for i in range(len(Str)):
            if Str[i] == '/':
                j.append(i)
        return j
    
    with open('lagouwangzhan.json','r', encoding='UTF-8-sig') as f:
#打开文件
        for i in range(line_num('lagouwangzhan.json')-1):
            f_each = f.readline()
            f_each_dict = js.loads(f_each[:-1])
             #json文件转换为字典
             #拆分字典文件到列表
             #拆分‘jobNeed’部分
            Str_jN = f_each_dict['jobNeed']
            Sp_1 = findSprit(Str_jN)
            jNeed_exp.append(Str_jN[2:Sp_1-1])
            jNeed_edu.append(Str_jN[Sp_1+2:])
            #拆分‘jobType’部分
            Str_jTy = f_each_dict['jobType']
            Sp_2 = findDobSprit(Str_jTy)
            Sp_2_1 = Sp_2[0]
            Sp_2_2 = Sp_2[1]
            jTy_type.append(Str_jTy[:Sp_2_1-1])
            jTy_financ.append(Str_jTy[Sp_2_1+2:Sp_2_2-1])
            jTy_size.append(Str_jTy[Sp_2_2+2:])
            #提取‘薪酬’部分
            Str_jM = f_each_dict['jobMoney'][0]
            jMoney.append(Str_jM)
            k_num = findSprit(Str_jM)
            jM_low.append(int(Str_jM[:k_num] + '000'))
            #数据处理
            #处理薪酬，将最低薪酬导入到字典 
    nd_jM_low = np.array(jM_low)
    jM_low_dict = {'5000元以下':0,'5000-10000元':0,'10000-15000元':0,'15000-20000元':0,'20000元以上':0}
    for i in range(len(jM_low)):
        if nd_jM_low[i]<5001:
            jM_low_dict['5000元以下'] += 1
        elif nd_jM_low[i]>5001 and jM_low[i]<10001:
            jM_low_dict['5000-10000元'] += 1
        elif nd_jM_low[i]>10001 and jM_low[i]<15001:
            jM_low_dict['10000-15000元'] += 1
        elif nd_jM_low[i]>15001 and jM_low[i]<20001:
            jM_low_dict['15000-20000元'] += 1
        else:
            jM_low_dict['20000元以上'] += 1
        #用Counter计数，返回字典
    jN_exp_dict = Counter(jNeed_exp)
    jN_edu_dict = Counter(jNeed_edu)
    jTy_size_dict = Counter(jTy_size)
    jTy_size_np = np.array(list(jTy_size_dict.values()))
    jTy_financ_dict = Counter(jTy_financ)
    jTy_financ_np = np.array(list(jTy_financ_dict.values()))
    #设置字体型号
    matplotlib.rcParams['font.family']=['SimHei']
    #职位工作经验要求条形图
    f=plt.figure(figsize=(36,20))
    
    plt.subplot(321)
    label_list=['应届毕业生','1年以下','1-3年','3-5年','5-10年','不限']
    H1=[jN_exp_dict['应届毕业生'],jN_exp_dict['1年以下'],jN_exp_dict['1-3年'],jN_exp_dict['3-5年'],jN_exp_dict['5-10年'],jN_exp_dict['不限']]
    x=range(len(H1))
    rects1 = plt.bar(left=x,height=H1,width=0.45,alpha=0.8,color='lightskyblue')
    plt.ylabel("需求人员数量(人)",fontsize=15)
    plt.xticks([index + 0.2 for index in x], label_list)
    plt.xlabel("工作经验(年)",fontsize=15)
    plt.title("职位工作经验要求",fontsize=25)
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
    #职位学历要求条形图
    plt.subplot(322)
    label_list=['不限','大专','本科','硕士','博士']
    H2=[jN_edu_dict['不限'],jN_edu_dict['大专'],jN_edu_dict['本科'],jN_edu_dict['硕士'],jN_edu_dict['博士']]
    x=range(len(H2))
    rects2 = plt.bar(left=x,height=H2,width=0.45,alpha=0.8,color='gold')
    plt.ylabel("需求人员数量(人)",fontsize=15)
    plt.xticks([index + 0.2 for index in x], label_list)
    plt.xlabel("学历",fontsize=15)
    plt.title("职位学历要求",fontsize=25)
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
    #公司规模饼图
    plt.subplot(323)
    label_list=['15-50人','50-150人','150-500人','500-2000人','2000人以上','少于15人']
    H3=sum(jTy_size_np)
    size=[jTy_size_dict['15-50人']/H3,jTy_size_dict['50-150人']/H3,jTy_size_dict['150-500人']/H3,jTy_size_dict['500-2000人']/H3,jTy_size_dict['2000人以上']/H3,
          jTy_size_dict['少于15人']/H3]
    color=["chocolate","yellowgreen","lightskyblue","gold","red","orange"]
    plt.pie(size,colors=color,labels=label_list,labeldistance=1.1,autopct="%1.1f%%",shadow=False,
                     startangle=90,pctdistance=0.6,textprops={'fontsize':12,'color':'w'})
    plt.title("公司规模",fontsize=25)
    plt.axis("equal")
    plt.legend(loc='upper right')
    plt.subplots_adjust(hspace =0.5)
    #公司融资情况饼图
    plt.subplot(324)
    label_list=['不需要融资','未融资','A轮','B轮','C轮','D轮及以上','天使轮','上市公司']
    H4=sum(jTy_financ_np)
    size=[jTy_financ_dict['不需要融资']/H4,jTy_financ_dict['未融资']/H4,jTy_financ_dict['A轮']/H4,jTy_financ_dict['B轮']/H4,jTy_financ_dict['C轮']/H4,
          jTy_financ_dict['D轮及以上']/H4,jTy_financ_dict['天使轮']/H4,jTy_financ_dict['上市公司']/H4]
    color=["pink","yellowgreen","lightskyblue","gold","orange","chocolate","slateblue","red"]
    plt.pie(size,colors=color,labels=label_list,labeldistance=1.1,autopct="%1.1f%%",shadow=False,
                     startangle=90,pctdistance=0.6,textprops={'fontsize':12,'color':'w'})
    plt.title("公司融资情况",fontsize=25)
    plt.axis("equal")
    plt.legend(loc='upper right')
    plt.subplots_adjust(hspace =0.5)
    #公司薪酬待遇饼图
    plt.subplot(325)
    label_list=['5000元以下','5000-10000元','10000-15000元','15000-20000元','20000元以上']
    H5=len(nd_jM_low)
    size=[jM_low_dict['5000元以下']/H5,jM_low_dict['5000-10000元']/H5,jM_low_dict['10000-15000元']/H5,jM_low_dict['15000-20000元']/H5,jM_low_dict['20000元以上']/H5]
    color=["pink","yellowgreen","lightskyblue","gold","red"]
    plt.pie(size,colors=color,labels=label_list,labeldistance=1.1,autopct="%1.1f%%",shadow=False,
                     startangle=90,pctdistance=0.6,textprops={'fontsize':12,'color':'w'})
    plt.title("公司薪酬待遇",fontsize=25)
    plt.axis("equal")
    plt.legend(loc='upper right')
    plt.subplots_adjust(hspace =0.5)
    
    return f

def paint1():
    
    global jN_exp_dict
    
    #设置字体型号
    matplotlib.rcParams['font.family']=['SimHei']                    
                    
    #职位工作经验要求条形图
    f1=plt.figure(num='fig1',figsize=(6,6),dpi=75,facecolor='#EEE9E9',edgecolor='#FFFAFA',frameon=False)
    label_list=['应届毕业生','1年以下','1-3年','3-5年','5-10年','不限']
    H1=[jN_exp_dict['应届毕业生'],jN_exp_dict['1年以下'],jN_exp_dict['1-3年'],jN_exp_dict['3-5年'],jN_exp_dict['5-10年'],jN_exp_dict['不限']]
    x=range(len(H1))
    rects1 = plt.bar(left=x,height=H1,width=0.45,alpha=0.8,color='lightskyblue')
    plt.ylabel("需求人员数量(人)",fontsize=15) 
    plt.xticks([index + 0.2 for index in x], label_list)
    plt.xlabel("工作经验(年)",fontsize=15)
    plt.title("职位工作经验要求",fontsize=25)
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
    return f1

def paint2():
    
    global jN_edu_dict
    
    #设置字体型号
    matplotlib.rcParams['font.family']=['SimHei']                    
                    
                    #职位工作经验要求条形图
    f2=plt.figure(num='fig2',figsize=(6,6),dpi=75,facecolor='#EEE9E9',edgecolor='#FFFAFA',frameon=False)
    label_list=['不限','大专','本科','硕士','博士']
    H2=[jN_edu_dict['不限'],jN_edu_dict['大专'],jN_edu_dict['本科'],jN_edu_dict['硕士'],jN_edu_dict['博士']]
    x=range(len(H2))
    rects2 = plt.bar(left=x,height=H2,width=0.45,alpha=0.8,color='gold')
    plt.ylabel("需求人员数量(人)",fontsize=15)
    plt.xticks([index + 0.2 for index in x], label_list)
    plt.xlabel("学历",fontsize=15)
    plt.title("职位学历要求",fontsize=25)
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom")
    return f2

def paint3():
    
    global jTy_size_dict
    global jTy_size_np
    
    #设置字体型号
    matplotlib.rcParams['font.family']=['SimHei']                    
                    
                    #职位工作经验要求条形图
    f3=plt.figure(num='fig3',figsize=(6,6),dpi=75)
    label_list=['15-50人','50-150人','150-500人','500-2000人','2000人以上','少于15人']
    H3=sum(jTy_size_np)
    size=[jTy_size_dict['15-50人']/H3,jTy_size_dict['50-150人']/H3,jTy_size_dict['150-500人']/H3,jTy_size_dict['500-2000人']/H3,jTy_size_dict['2000人以上']/H3,
          jTy_size_dict['少于15人']/H3]
    color=["chocolate","yellowgreen","lightskyblue","gold","red","orange"]
    plt.pie(size,colors=color,labels=label_list,labeldistance=1.1,autopct="%1.1f%%",shadow=False,
                     startangle=90,pctdistance=0.6,textprops={'fontsize':12,'color':'w'})
    plt.title("公司规模",fontsize=25)
    plt.axis("equal")
    plt.legend(loc='upper right')
    return f3

def paint4():

    global jTy_financ_dict
    global jTy_financ_np
    
    #设置字体型号
    matplotlib.rcParams['font.family']=['SimHei']                    
                    
                    #职位工作经验要求条形图
    f4=plt.figure(num='fig4',figsize=(6,6),dpi=75)
    label_list=['不需要融资','未融资','A轮','B轮','C轮','D轮及以上','天使轮','上市公司']
    H4=sum(jTy_financ_np)
    size=[jTy_financ_dict['不需要融资']/H4,jTy_financ_dict['未融资']/H4,jTy_financ_dict['A轮']/H4,jTy_financ_dict['B轮']/H4,jTy_financ_dict['C轮']/H4,
          jTy_financ_dict['D轮及以上']/H4,jTy_financ_dict['天使轮']/H4,jTy_financ_dict['上市公司']/H4]
    color=["pink","yellowgreen","lightskyblue","gold","orange","chocolate","slateblue","red"]
    plt.pie(size,colors=color,labels=label_list,labeldistance=1.1,autopct="%1.1f%%",shadow=False,
                     startangle=90,pctdistance=0.6,textprops={'fontsize':12,'color':'w'})
    plt.title("公司融资情况",fontsize=25)
    plt.axis("equal")
    plt.legend(loc='upper right')
    return f4

def paint5():
    
    global jM_low_dict
    global nd_jM_low
    
    #设置字体型号
    matplotlib.rcParams['font.family']=['SimHei']                    
                    
                    #职位工作经验要求条形图
    f5=plt.figure(num='fig5',figsize=(6,6),dpi=75)
    plt.figure(num='fig5',figsize=(6,6),dpi=75)
    label_list=['5000元以下','5000-10000元','10000-15000元','15000-20000元','20000元以上']
    H5=len(nd_jM_low)
    size=[jM_low_dict['5000元以下']/H5,jM_low_dict['5000-10000元']/H5,jM_low_dict['10000-15000元']/H5,jM_low_dict['15000-20000元']/H5,jM_low_dict['20000元以上']/H5]
    color=["pink","yellowgreen","lightskyblue","gold","red"]
    plt.pie(size,colors=color,labels=label_list,labeldistance=1.1,autopct="%1.1f%%",shadow=False,
                     startangle=90,pctdistance=0.6,textprops={'fontsize':12,'color':'w'})
    plt.title("公司薪酬待遇",fontsize=25)
    plt.axis("equal")
    plt.legend(loc='upper right')
    return f5


  

def login():
    usr_name = name.get()
    usr_pwd = password.get()
    try:
        with open('users.pickle', 'rb') as usr_file:
            users = pickle.load(usr_file)
    except FileNotFoundError:
        with open('users.pickle', 'wb') as usr_file:
            users = {'qzy': 'qzy'}
            pickle.dump(users, usr_file)
    if usr_name in users:
        if usr_pwd == users[usr_name]:
            window.destroy()
            window_spider_paint = tk.Tk() 
          
            window_spider_paint.geometry('300x500')
            window_spider_paint.title('欢迎使用')

            canvas = tk.Canvas(window_spider_paint,bg = '#a55dff' ,height=500, width=80)
            canvas.pack(side='left')
           
            
            
           
            spider_a = False
            paint_a =False

            def spider():
                global spider_a
                spider_a = tk.messagebox.askokcancel('爬虫', '开始使用爬虫?')
                if spider_a:                  
                    os.system(r'scrapy crawl second')
                               
                else:
                    pass
    
            def paint():
                global paint_a
                paint_a = tk.messagebox.askokcancel('绘图','开始分析绘图?')
                if paint_a:
                    
                    
                    window_spider_paint.destroy()
                    window_paint = tk.Tk() 
          
                    window_paint.geometry('1400x900')
                    window_paint.title('绘图')
                    frm=tk.Frame(window_paint)
                    frm.pack()
             
                    frm_l = tk.Frame(frm)
                    frm_r = tk.Frame(frm)
                    frm_l.pack(side =  'left')
                    frm_r.pack(side = 'right')
                    ff=analysis()
                    canvas=FigureCanvasTkAgg(ff,frm_r)
                    canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
                    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                    
                    
                    def paint11():
                        
                        ff1 = paint1()
                        
                        window_paint1 = tk.Tk() 

                        window_paint1.geometry('500x500')
                        window_paint1.title('绘图')
                        frm=tk.Frame(window_paint1)
                        frm.pack()

                        frm_l = tk.Frame(frm)
                        frm_r = tk.Frame(frm)
                        frm_l.pack(side =  'left')
                        frm_r.pack(side = 'right')
                       
                        
                        canvas=FigureCanvasTkAgg(ff1,frm_r)
                        canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
                        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                        toolbar =NavigationToolbar2Tk(canvas, window_paint1) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
                        toolbar.update()
                        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                    def paint12():
                        
                        ff1 = paint2()
                        
                        window_paint1 = tk.Tk() 

                        window_paint1.geometry('500x500')
                        window_paint1.title('绘图')
                        frm=tk.Frame(window_paint1)
                        frm.pack()

                        frm_l = tk.Frame(frm)
                        frm_r = tk.Frame(frm)
                        frm_l.pack(side =  'left')
                        frm_r.pack(side = 'right')
                       
                        
                        canvas=FigureCanvasTkAgg(ff1,frm_r)
                        canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
                        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                        toolbar =NavigationToolbar2Tk(canvas, window_paint1) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
                        toolbar.update()
                        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                    def paint13():
                        
                        ff1 = paint3()
                        
                        window_paint1 = tk.Tk() 

                        window_paint1.geometry('500x500')
                        window_paint1.title('绘图')
                        frm=tk.Frame(window_paint1)
                        frm.pack()

                        frm_l = tk.Frame(frm)
                        frm_r = tk.Frame(frm)
                        frm_l.pack(side =  'left')
                        frm_r.pack(side = 'right')
                       
                        
                        canvas=FigureCanvasTkAgg(ff1,frm_r)
                        canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
                        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                        toolbar =NavigationToolbar2Tk(canvas, window_paint1) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
                        toolbar.update()
                        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                    def paint14():
                        
                        ff1 = paint4()
                        
                        window_paint1 = tk.Tk() 

                        window_paint1.geometry('500x500')
                        window_paint1.title('绘图')
                        frm=tk.Frame(window_paint1)
                        frm.pack()

                        frm_l = tk.Frame(frm)
                        frm_r = tk.Frame(frm)
                        frm_l.pack(side =  'left')
                        frm_r.pack(side = 'right')
                       
                        
                        canvas=FigureCanvasTkAgg(ff1,frm_r)
                        canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
                        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                        toolbar =NavigationToolbar2Tk(canvas, window_paint1) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
                        toolbar.update()
                        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                    def paint15():
                        
                        ff1 = paint5()
                        
                        window_paint1 = tk.Tk() 

                        window_paint1.geometry('500x500')
                        window_paint1.title('绘图')
                        frm=tk.Frame(window_paint1)
                        frm.pack()

                        frm_l = tk.Frame(frm)
                        frm_r = tk.Frame(frm)
                        frm_l.pack(side =  'left')
                        frm_r.pack(side = 'right')
                       
                        
                        canvas=FigureCanvasTkAgg(ff1,frm_r)
                        canvas.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
                        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                        toolbar =NavigationToolbar2Tk(canvas, window_paint1) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
                        toolbar.update()
                        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
                    
                    btn_paint = tk.Button(frm_l,font=ftt,text = '绘图1',bg='white',command = paint11,width= 10).pack()
                    btn_paint = tk.Button(frm_l,font=ftt,text = '绘图2',bg='#5d8fff',command = paint12,width= 10).pack()
                    btn_paint = tk.Button(frm_l,font=ftt,text = '绘图3',bg='white',command = paint13,width= 10).pack()
                    btn_paint = tk.Button(frm_l,font=ftt,text = '绘图4',bg='#5d8fff',command = paint14,width= 10).pack()
                    btn_paint = tk.Button(frm_l,font=ftt,text = '绘图5',bg='white',command = paint15,width= 10).pack()
                else:
                    pass

            btn_spider = tk.Button(window_spider_paint,font=ftt,text = '爬虫',command = spider,width = 10)
            btn_spider.place(x= 130,y=140)
            btn_paint = tk.Button(window_spider_paint,font=ftt,text = '分析与绘图',command = paint,width = 10)
            btn_paint.place(x= 130,y=270)
            
        else:
            tk.messagebox.showerror(message='密码输入错误！')
    else:
        is_sign = tk.messagebox.askyesno('登录','你还没有注册，现在注册吗?')
        if is_sign:
            sign_up()

def sign_up():
    def sign_to():
        np = new_pwd.get()
        nn = new_name.get()
        npf = new_pwd_confirm.get()
        with open('users.pickle', 'rb') as usr_file:
            usr_info = pickle.load(usr_file)
        if np != npf:
            tk.messagebox.showerror('', '密码前后不一致！')
        elif nn in usr_info:
            tk.messagebox.showerror('','该用户名已被使用!')
        else:
            usr_info[nn] = np
            with open('users.pickle', 'wb') as usr_file:
                pickle.dump(usr_info, usr_file)
            tk.messagebox.showinfo('','注册成功!')
            window_sign_up.destroy()

    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('400x500')
    window_sign_up.title('注册')
    canvas = tk.Canvas(window_sign_up,bg='#5d8fff' ,height=600, width=70)

    canvas.pack(side='left')
    new_name = tk.StringVar()
    new_name.set('')
    tk.Label(window_sign_up, font=ft,text='用户名: ').place(x=90, y= 70)
    enew_name = tk.Entry(window_sign_up, textvariable=new_name)
    enew_name.place(x=210, y=70)

    
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, font=ft,text='密码: ').place(x=90, y=140)
    eusr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    eusr_pwd.place(x=210, y=140)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, font=ft,text='再次输入: ').place(x=90, y=210)
    eusr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    eusr_pwd.place(x=210, y=210)

    new_email = tk.StringVar()
    tk.Label(window_sign_up, font=ft,text='电子邮箱: ').place(x=90, y=280)
    eusr_pwd = tk.Entry(window_sign_up, textvariable=new_email)
    eusr_pwd.place(x=210, y=280)

    btn_sign_up = tk.Button(window_sign_up, font=ftt,text='注册', command=sign_to,width = 10)
    btn_sign_up.place(x=210, y=350)


b1 = tk.Button(window, font=ftt,text='登录', command=login,width = 10)
b1.place(x=100, y=230)
b2 = tk.Button(window,font=ftt, text='注册', command=sign_up,width = 10)
b2.place(x=270, y=230)

window.mainloop()