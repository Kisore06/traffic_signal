from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
import base64
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
import math
import sys

import cv2
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import threading
import os
import time
import shutil
import imagehash
import hashlib
import PIL.Image
from PIL import Image
from PIL import ImageTk
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import argparse
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="traffic_signal"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    ff=open("det.txt","w")
    ff.write("1")
    ff.close()

    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()

    ff11=open("img.txt","w")
    ff11.write("1")
    ff11.close()

    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff11=open("title2.txt","r")
    title2=ff11.read()
    ff11.close()

    #shutil.copy("static/vehicle/cc1.jpg","static/assets/img/d1/cc1.des")

    #shutil.copy("static/assets/img/d1/cc1.des","static/assets/img/d1/a.jpg")
        

    return render_template('index.html',msg=msg,act=act,title=title,title1=title1,title2=title2)

@app.route('/login', methods=['POST','GET'])
def login():
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff11=open("title2.txt","r")
    title2=ff11.read()
    ff11.close()
    
    if request.method == 'POST':
        uname = request.form['uname']
        pass1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ap_admin where username=%s && password=%s && utype='2'",(uname,pass1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            
            session['username'] = uname
            
            return redirect(url_for('nhai_home')) 
        else:
            msg="Incorrect username/password!!!"
                
    
    return render_template('login.html',msg=msg,title=title,title1=title1,title2=title2)

@app.route('/login_user', methods=['POST','GET'])
def login_user():
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff11=open("title2.txt","r")
    title2=ff11.read()
    ff11.close()
    
    if request.method == 'POST':
        uname = request.form['uname']
        pass1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ap_register where uname=%s && pass=%s",(uname,pass1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            
            session['username'] = uname
            
            return redirect(url_for('userhome')) 
        else:
            msg="Incorrect username/password!!!"
                
    
    return render_template('login_user.html',msg=msg,title=title,title1=title1,title2=title2)

@app.route('/login_admin', methods=['POST','GET'])
def login_admin():
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff11=open("title2.txt","r")
    title2=ff11.read()
    ff11.close()
    
    
    if request.method == 'POST':
        uname = request.form['uname']
        pass1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ap_admin where username=%s && password=%s && utype='1'",(uname,pass1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            session['username'] = uname
            
            return redirect(url_for('register')) 
        else:
            msg="You are logged in fail!!!"
                
    
    return render_template('login_admin.html',msg=msg,title=title,title1=title1,title2=title2)

@app.route('/login2', methods=['POST','GET'])
def login2():
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff11=open("title2.txt","r")
    title2=ff11.read()
    ff11.close()
    
    if request.method == 'POST':
        uname = request.form['uname']
        pass1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM ap_traffic where uname=%s && pass=%s",(uname,pass1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            session['username'] = uname
            ff1=open("log.txt","w")
            ff1.write(uname)
            ff1.close()
            return redirect(url_for('admin_control')) 
        else:
            msg="You are logged in fail!!!"
                
    
    return render_template('login2.html',msg=msg,title=title,title1=title1,title2=title2)

def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m

@app.route('/vehicle_count', methods=['POST','GET'])
def vehicle_count():
    msg=""
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    '''path_main = 'static/vehicle'
    for fname in os.listdir(path_main):
        fa=fname.split(".")
        fa2=fa[0]+".des"
        shutil.copy("static/d1/"+fname,"static/process1/"+fa2)'''

    path_main = 'static/process3'
    for fname in os.listdir(path_main):
        if fname=="":
            s=1
        else:
            os.remove("static/process3/"+fname)
           


    return render_template('vehicle_count.html',msg=msg,title=title,title1=title1)


@app.route('/process1', methods=['POST','GET'])
def process1():
    msg=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()


    '''path_main = 'static/vehicle'
    for fname in os.listdir(path_main):
        fa=fname.split(".")
        fa2=fa[0]+".des"
        shutil.copy("static/d1/"+fname,"static/process1/"+fa2)'''

    path_main = 'static/process3'
    for fname in os.listdir(path_main):
        if fname=="":
            s=1
        else:
            os.remove("static/process3/"+fname)
            

    if request.method == 'POST':
        s=1
        ff=open("static/det.txt","r")
        fn1=ff.read()
        ff.close()
        
        ff=open("static/cycle.txt","w")
        ff.write("1")
        ff.close()

        fn11=fn1.split(",")
        #print(fn11)

        for fn22 in fn11:
            fn3=fn22.split("-")
            fnn.append(fn3[0])
            fc.append(fn3[1])

        
        path_main = 'static/process1'
        for fname in os.listdir(path_main):
            
            fa=fname.split(".")
            for fnn1 in fnn:
                fnn2=fnn1.split(".")
                if fa[0]==fnn2[0]:
                    fa2=fa[0]+"."+fnn2[1]
                    shutil.copy("static/process1/"+fname,"static/process3/"+fa2)

        return redirect(url_for('process2'))

    return render_template('process1.html',msg=msg,title=title,title1=title1)

@app.route('/process2', methods=['POST','GET'])
def process2():
    msg=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    view=request.args.get("view")
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    path_main = 'static/process3'
    for fname in os.listdir(path_main):
        if fname=="":
            s=1
        else:
            os.remove("static/process3/"+fname)
    if act=="1":
        s=1
        ff=open("static/det.txt","r")
        fn1=ff.read()
        ff.close()

        fn11=fn1.split(",")
        #print(fn11)

        for fn22 in fn11:
            fn3=fn22.split("-")
            fnn.append(fn3[0])
            fc.append(fn3[1])

        
        path_main = 'static/process1'
        for fname in os.listdir(path_main):
            
            fa=fname.split(".")
            for fnn1 in fnn:
                fnn2=fnn1.split(".")
                if fa[0]==fnn2[0]:
                    fa2=fa[0]+"."+fnn2[1]
                    shutil.copy("static/process1/"+fname,"static/process3/"+fa2)


    

    return render_template('process2.html',msg=msg,view=view,title=title,title1=title1)

@app.route('/pro1', methods=['POST','GET'])
def pro1():
    msg=""
    st=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff=open("static/det.txt","r")
    fn1=ff.read()
    ff.close()

    fn11=fn1.split(",")
    #print(fn11)

    for fn22 in fn11:
        fn3=fn22.split("-")
        fnn.append(fn3[0])
        fc.append(fn3[1])

    if act=="1":
        print("act")
        s=1
        ff=open("static/det.txt","r")
        fn1=ff.read()
        ff.close()

        fn11=fn1.split(",")
        #print(fn11)

        for fn22 in fn11:
            fn3=fn22.split("-")
            fnn.append(fn3[0])
            fc.append(fn3[1])

        
        path_main = 'static/process1'
        for fname in os.listdir(path_main):
            
            fa=fname.split(".")
            for fnn1 in fnn:
                fnn2=fnn1.split(".")
                if fa[0]==fnn2[0]:
                    fa2=fa[0]+"."+fnn2[1]
                    shutil.copy("static/process1/"+fname,"static/process3/"+fa2)
                    
        
        mycursor = mydb.cursor()
        
        a=int(fc[0])
        b=int(fc[1])
        c=int(fc[2])
        d=int(fc[3])

        mycursor.execute("update ap_temp set value1=%s where id=1",(a,))
        mydb.commit()

        mycursor.execute("update ap_temp set value1=%s where id=2",(b,))
        mydb.commit()

        mycursor.execute("update ap_temp set value1=%s where id=3",(c,))
        mydb.commit()

        mycursor.execute("update ap_temp set value1=%s where id=4",(d,))
        mydb.commit()
        
        sg=[]
        cnt=0
        low=0
        mycursor.execute("SELECT count(*) from ap_temp where id<=4 && value1<=3")
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            sg1=""
            mycursor.execute("SELECT * from ap_temp where id<=4 && value1<=3")
            ds = mycursor.fetchall()
            for ds1 in ds:
                low=ds1[0]
                if low==1:
                    sg1="A,B1,C1,D1"
                elif low==2:
                    sg1="A1,B,C1,D1"
                elif low==3:
                    sg1="A1,B1,C,D1"
                elif low==4:
                    sg1="A1,B1,C1,D"
            sg.append(sg1)
            
        
            mycursor.execute("SELECT * from ap_temp where id<=4 && id!=%s order by value1 desc",(low,))
            myres = mycursor.fetchall()
            for myres1 in myres:
                sg1=""
                if myres1[0]==1:
                    sg1="A,B1,C1,D1"
                elif myres1[0]==2:
                    sg1="A1,B,C1,D1"
                elif myres1[0]==3:
                    sg1="A1,B1,C,D1"
                elif myres1[0]==4:
                    sg1="A1,B1,C1,D"

                sg.append(sg1)
        else:
            mycursor.execute("SELECT * from ap_temp where id<=4 order by value1 desc")
            myres = mycursor.fetchall()
            for myres1 in myres:
                sg1=""
                if myres1[0]==1:
                    sg1="A,B1,C1,D1"
                elif myres1[0]==2:
                    sg1="A1,B,C1,D1"
                elif myres1[0]==3:
                    sg1="A1,B1,C,D1"
                elif myres1[0]==4:
                    sg1="A1,B1,C1,D"

                sg.append(sg1)

        sig='|'.join(sg)
        ff=open("static/signal.txt","w")
        ff.write(sig)
        ff.close()

        
        
    elif act=="2":
        s=1
        ff=open("static/det.txt","r")
        fn1=ff.read()
        ff.close()

        ff=open("static/signal.txt","r")
        sig=ff.read()
        ff.close()

        fn11=fn1.split(",")
        #print(fn11)

        for fn22 in fn11:
            fn3=fn22.split("-")
            fnn.append(fn3[0])
            fc.append(fn3[1])

        sig1=sig.split("|")

        if sgn=="1":
            svalue=sig1[0].split(',')
            
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3]
            
        elif sgn=="2":
            svalue=sig1[1].split(',')
            signal="B"
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3]
        elif sgn=="3":
            svalue=sig1[2].split(',')
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3]
        elif sgn=="4":
            svalue=sig1[3].split(',')
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3] 
    
        if signal1=="A":
            signal="A"
        elif signal2=="B":
            signal="B"
        elif signal3=="C":
            signal="C"
        elif signal4=="D":
            signal="D"
        
            
        
    else:

        ##    
        ff2=open("static/assets/vendor/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        ex=dat.split('|')
        
        ##
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * from ap_temp order by rand()")
        myres = mycursor.fetchall()
        i=1
        rnb=[]
        for myres1 in myres:
            if i<=4:
                rnb.append(myres1[0])
            i+=1 
        #rn1=randint(1,10)
        #rn2=randint(1,10)
        #rn3=randint(1,10)
        #rn4=randint(1,10)
        rn1=rnb[0]
        rn2=rnb[1]
        rn3=rnb[2]
        rn4=rnb[3]

        fn1=ex[rn1-1]
        fn2=ex[rn2-1]
        fn3=ex[rn3-1]
        fn4=ex[rn4-1]

        fdata=fn1+","+fn2+","+fn3+","+fn4
        ff=open("static/det.txt","w")
        ff.write(fdata)
        ff.close()

        fn11=fn1.split("-")
        fn22=fn2.split("-")
        fn33=fn3.split("-")
        fn44=fn4.split("-")

        fnn.append(fn11[0])
        fnn.append(fn22[0])
        fnn.append(fn33[0])
        fnn.append(fn44[0])

    '''ff=open("static/cycle.txt","r")
    new_cycle=ff.read()
    ff.close()
    ####
    if new_cycle=="1":
        ##    
        ff2=open("static/assets/vendor/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            num.append(int(r1[i]))
            i+=1

        ####
        ff=open("static/cycle.txt","r")
        new_cycle=ff.read()
        ff.close()
        ####
        dat=toString(num)
        dd2=[]
        ex=dat.split('|')
        
        ##
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * from ap_temp order by rand()")
        myres = mycursor.fetchall()
        i=1
        rnb=[]
        for myres1 in myres:
            if i<=4:
                rnb.append(myres1[0])
            i+=1 
        #rn1=randint(1,10)
        #rn2=randint(1,10)
        #rn3=randint(1,10)
        #rn4=randint(1,10)
        rn1=rnb[0]
        rn2=rnb[1]
        rn3=rnb[2]
        rn4=rnb[3]

        fn1=ex[rn1-1]
        fn2=ex[rn2-1]
        fn3=ex[rn3-1]
        fn4=ex[rn4-1]

        fdata=fn1+","+fn2+","+fn3+","+fn4
        ff=open("static/det.txt","w")
        ff.write(fdata)
        ff.close()

        fn11=fn1.split("-")
        fn22=fn2.split("-")
        fn33=fn3.split("-")
        fn44=fn4.split("-")

        fnn.append(fn11[0])
        fnn.append(fn22[0])
        fnn.append(fn33[0])
        fnn.append(fn44[0])

        ff=open("static/cycle.txt","w")
        ff.write("2")
        ff.close()'''

            

    return render_template('pro1.html',msg=msg,act=act,title=title,title1=title1,fnn=fnn,fc=fc,st=st)

@app.route('/pro2', methods=['POST','GET'])
def pro2():
    msg=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]

    ff=open("static/cycle.txt","r")
    new_cycle=ff.read()
    ff.close()

    
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff=open("static/det.txt","r")
    fn1=ff.read()
    ff.close()

    fn11=fn1.split(",")
    #print(fn11)

    ff=open("static/cycle.txt","r")
    new_cycle=ff.read()
    ff.close()

    for fn22 in fn11:
        fn3=fn22.split("-")
        fnn.append(fn3[0])
        fc.append(fn3[1])


    
    return render_template('pro2.html',msg=msg,act=act,title=title,title1=title1,fnn=fnn,fc=fc)

@app.route('/pro3', methods=['POST','GET'])
def pro3():
    msg=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff=open("static/det.txt","r")
    fn1=ff.read()
    ff.close()

    fn11=fn1.split(",")
    #print(fn11)

    for fn22 in fn11:
        fn3=fn22.split("-")
        fnn.append(fn3[0])
        fc.append(fn3[1])
        

    return render_template('pro3.html',msg=msg,act=act,title=title,title1=title1,fnn=fnn,fc=fc)

@app.route('/pro4', methods=['POST','GET'])
def pro4():
    msg=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff=open("static/det.txt","r")
    fn1=ff.read()
    ff.close()

    fn11=fn1.split(",")
    #print(fn11)

    for fn22 in fn11:
        fn3=fn22.split("-")
        fnn.append(fn3[0])
        fc.append(fn3[1])

    return render_template('pro4.html',msg=msg,act=act,title=title,title1=title1,fnn=fnn,fc=fc)

@app.route('/pro5', methods=['POST','GET'])
def pro5():
    msg=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff=open("static/det.txt","r")
    fn1=ff.read()
    ff.close()

    fn11=fn1.split(",")
    #print(fn11)

    for fn22 in fn11:
        fn3=fn22.split("-")
        fnn.append(fn3[0])
        fc.append(fn3[1])

    ff=open("static/signal.txt","r")
    sig=ff.read()
    ff.close()

    sig1=sig.split("|")

    if sgn=="1":
        svalue=sig1[0].split(',')
        
        signal1=svalue[0]
        signal2=svalue[1]
        signal3=svalue[2]
        signal4=svalue[3]
        
    elif sgn=="2":
        svalue=sig1[1].split(',')
        signal="B"
        signal1=svalue[0]
        signal2=svalue[1]
        signal3=svalue[2]
        signal4=svalue[3]
    elif sgn=="3":
        svalue=sig1[2].split(',')
        signal1=svalue[0]
        signal2=svalue[1]
        signal3=svalue[2]
        signal4=svalue[3]
    elif sgn=="4":
        svalue=sig1[3].split(',')
        signal1=svalue[0]
        signal2=svalue[1]
        signal3=svalue[2]
        signal4=svalue[3] 

    if signal1=="A":
        signal="A"
    elif signal2=="B":
        signal="B"
    elif signal3=="C":
        signal="C"
    elif signal4=="D":
        signal="D"
        

    return render_template('pro5.html',msg=msg,act=act,title=title,title1=title1,fnn=fnn,fc=fc,signal=signal,sgn=sgn,signal1=signal1,signal2=signal2,signal3=signal3,signal4=signal4,page=page)



@app.route('/process', methods=['POST','GET'])
def process():
    msg=""
    signal=""
    signal1=""
    signal2=""
    signal3=""
    signal4=""
    sgn=request.args.get("sgn")
    
    fnn=[]
    fc=[]
    act=request.args.get("act")
    page=request.args.get("page")
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    if act=="1":
        s=1
        ff=open("static/det.txt","r")
        fn1=ff.read()
        ff.close()

        fn11=fn1.split(",")
        #print(fn11)

        for fn22 in fn11:
            fn3=fn22.split("-")
            fnn.append(fn3[0])
            fc.append(fn3[1])

        
        path_main = 'static/process1'
        for fname in os.listdir(path_main):
            
            fa=fname.split(".")
            for fnn1 in fnn:
                fnn2=fnn1.split(".")
                if fa[0]==fnn2[0]:
                    fa2=fa[0]+"."+fnn2[1]
                    shutil.copy("static/process1/"+fname,"static/process3/"+fa2)
                    
        
        mycursor = mydb.cursor()
        
        a=int(fc[0])
        b=int(fc[1])
        c=int(fc[2])
        d=int(fc[3])

        mycursor.execute("update ap_temp set value1=%s where id=1",(a,))
        mydb.commit()

        mycursor.execute("update ap_temp set value1=%s where id=2",(b,))
        mydb.commit()

        mycursor.execute("update ap_temp set value1=%s where id=3",(c,))
        mydb.commit()

        mycursor.execute("update ap_temp set value1=%s where id=4",(d,))
        mydb.commit()
        
        sg=[]
        cnt=0
        low=0
        mycursor.execute("SELECT count(*) from ap_temp where id<=4 && value1<=3")
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            sg1=""
            mycursor.execute("SELECT * from ap_temp where id<=4 && value1<=3")
            ds = mycursor.fetchall()
            for ds1 in ds:
                low=ds1[0]
                if low==1:
                    sg1="A,B1,C1,D1"
                elif low==2:
                    sg1="A1,B,C1,D1"
                elif low==3:
                    sg1="A1,B1,C,D1"
                elif low==4:
                    sg1="A1,B1,C1,D"
            sg.append(sg1)
            
        
            mycursor.execute("SELECT * from ap_temp where id<=4 && id!=%s order by value1 desc",(low,))
            myres = mycursor.fetchall()
            for myres1 in myres:
                sg1=""
                if myres1[0]==1:
                    sg1="A,B1,C1,D1"
                elif myres1[0]==2:
                    sg1="A1,B,C1,D1"
                elif myres1[0]==3:
                    sg1="A1,B1,C,D1"
                elif myres1[0]==4:
                    sg1="A1,B1,C1,D"

                sg.append(sg1)
        else:
            mycursor.execute("SELECT * from ap_temp where id<=4 order by value1 desc")
            myres = mycursor.fetchall()
            for myres1 in myres:
                sg1=""
                if myres1[0]==1:
                    sg1="A,B1,C1,D1"
                elif myres1[0]==2:
                    sg1="A1,B,C1,D1"
                elif myres1[0]==3:
                    sg1="A1,B1,C,D1"
                elif myres1[0]==4:
                    sg1="A1,B1,C1,D"

                sg.append(sg1)

        sig='|'.join(sg)
        ff=open("static/signal.txt","w")
        ff.write(sig)
        ff.close()

        
        
    elif act=="2":
        s=1
        ff=open("static/det.txt","r")
        fn1=ff.read()
        ff.close()

        ff=open("static/signal.txt","r")
        sig=ff.read()
        ff.close()

        fn11=fn1.split(",")
        #print(fn11)

        for fn22 in fn11:
            fn3=fn22.split("-")
            fnn.append(fn3[0])
            fc.append(fn3[1])

        sig1=sig.split("|")

        if sgn=="1":
            svalue=sig1[0].split(',')
            
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3]
            
        elif sgn=="2":
            svalue=sig1[1].split(',')
            signal="B"
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3]
        elif sgn=="3":
            svalue=sig1[2].split(',')
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3]
        elif sgn=="4":
            svalue=sig1[3].split(',')
            signal1=svalue[0]
            signal2=svalue[1]
            signal3=svalue[2]
            signal4=svalue[3] 
    
        if signal1=="A":
            signal="A"
        elif signal2=="B":
            signal="B"
        elif signal3=="C":
            signal="C"
        elif signal4=="D":
            signal="D"
        
            
        
    else:

        ##    
        ff2=open("static/assets/vendor/tdata.txt","r")
        rd=ff2.read()
        ff2.close()

        num=[]
        r1=rd.split(',')
        s=len(r1)
        ss=s-1
        i=0
        while i<ss:
            num.append(int(r1[i]))
            i+=1

        #print(num)
        dat=toString(num)
        dd2=[]
        ex=dat.split('|')
        
        ##
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * from ap_temp order by rand()")
        myres = mycursor.fetchall()
        i=1
        rnb=[]
        for myres1 in myres:
            if i<=4:
                rnb.append(myres1[0])
            i+=1 
        #rn1=randint(1,10)
        #rn2=randint(1,10)
        #rn3=randint(1,10)
        #rn4=randint(1,10)
        rn1=rnb[0]
        rn2=rnb[1]
        rn3=rnb[2]
        rn4=rnb[3]

        fn1=ex[rn1-1]
        fn2=ex[rn2-1]
        fn3=ex[rn3-1]
        fn4=ex[rn4-1]

        fdata=fn1+","+fn2+","+fn3+","+fn4
        ff=open("static/det.txt","w")
        ff.write(fdata)
        ff.close()

        fn11=fn1.split("-")
        fn22=fn2.split("-")
        fn33=fn3.split("-")
        fn44=fn4.split("-")

        fnn.append(fn11[0])
        fnn.append(fn22[0])
        fnn.append(fn33[0])
        fnn.append(fn44[0])
    


    return render_template('process.html',msg=msg,act=act,page=page,title=title,title1=title1,fnn=fnn,fc=fc,signal=signal,sgn=sgn,signal1=signal1,signal2=signal2,signal3=signal3,signal4=signal4)

#Q-Learning
def DeepQLearning(self,num_of_data):
        
    enviroment = "Traffic"
    action_space="1"
    action=0
    alpha=1
    reward=0
    
    for customer in range(0, num_of_data):
        # Reset the enviroment
        state = enviroment

        # Initialize variables
        reward = 0
        terminated = False
        j=1
        n=num_of_data
        while j<n:
            # Take learned path or explore new actions based on the epsilon
            if random.uniform(0, 1) < num_of_data:
                i=0
                k=0
                while i<=num_of_data:
                    i+=3
                    k+=1
                action = i
            else:
                action = np.argmax(q_table[state])

            # Take action
            gamma=1
            #next_state, reward, terminated, info = action
            q_table=num_of_data/3
            # Recalculate
            q_value = k
            max_value = q_table #np.max(q_table[next_state])
            new_q_value = (1 - alpha) * int(q_value) + alpha * (reward + gamma * max_value)
            
            # Update Q-table
            #q_table[state, action] = new_q_value
            state = new_q_value
            j+=1
            
        #if (queue + 1) % 100 == 0:
        #    clear_output(wait=True)
            #print("Queue: {}".format(queue + 1))
            #enviroment.render()

def QueuePredict(self,enviroment, optimizer):
        
        # Initialize atributes
        _state_size = enviroment
        _action_size = "1" #enviroment.action_space.n
        _optimizer = optimizer
        
        expirience_replay = int(enviroment/2)
        
        # Initialize discount and exploration rate
        gamma = 0.6
        epsilon = 0.1
        
        # Build networks
        q_network = optimizer
        target_network = expirience_replay
        

def store(self,state, action, reward, next_state, terminated):
    expirience_replay.append((state, action, reward, next_state, terminated))

def _build_compile_model(self):
    model = Sequential()
    model.add(Embedding(_state_size, 10, input_length=1))
    model.add(Reshape((10,)))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(_action_size, activation='linear'))
    
    model.compile(loss='mse', optimizer=self._optimizer)
    return model

def alighn_target_model(self):
    target_network.set_weights(q_network.get_weights())

def act(self,state):
    if np.random.rand() <= epsilon:
        return enviroment.action_space.sample()
    
    q_values = q_network.predict(state)
    return np.argmax(q_values[0])

def retrain(self,batch_size):
    minibatch = random.sample(expirience_replay, batch_size)
    
    for state, action, reward, next_state, terminated in minibatch:
        
        target = q_network.predict(state)
        
        if terminated:
            target[0][action] = reward
        else:
            t = target_network.predict(next_state)
            target[0][action] = reward + gamma * np.amax(t)
        
        q_network.fit(state, target, epochs=1, verbose=0)
            
def CNN():
    #Lets start by loading the Cifar10 data
    (X, y), (X_test, y_test) = cifar10.load_data()

    #Keep in mind the images are in RGB
    #So we can normalise the data by diving by 255
    #The data is in integers therefore we need to convert them to float first
    X, X_test = X.astype('float32')/255.0, X_test.astype('float32')/255.0

    #Then we convert the y values into one-hot vectors
    #The cifar10 has only 10 classes, thats is why we specify a one-hot
    #vector of width/class 10
    y, y_test = u.to_categorical(y, 10), u.to_categorical(y_test, 10)

    #Now we can go ahead and create our Convolution model
    model = Sequential()
    #We want to output 32 features maps. The kernel size is going to be
    #3x3 and we specify our input shape to be 32x32 with 3 channels
    #Padding=same means we want the same dimensional output as input
    #activation specifies the activation function
    model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), padding='same',
                     activation='relu'))
    #20% of the nodes are set to 0
    model.add(Dropout(0.2))
    #now we add another convolution layer, again with a 3x3 kernel
    #This time our padding=valid this means that the output dimension can
    #take any form
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    #maxpool with a kernet of 2x2
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #In a convolution NN, we neet to flatten our data before we can
    #input it into the ouput/dense layer
    model.add(Flatten())
    #Dense layer with 512 hidden units
    model.add(Dense(512, activation='relu'))
    #this time we set 30% of the nodes to 0 to minimize overfitting
    model.add(Dropout(0.3))
    #Finally the output dense layer with 10 hidden units corresponding to
    #our 10 classe
    model.add(Dense(10, activation='softmax'))
    #Few simple configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(momentum=0.5, decay=0.0004), metrics=['accuracy'])
    #Run the algorithm!
    model.fit(X, y, validation_data=(X_test, y_test), epochs=25,
              batch_size=512)
    #Save the weights to use for later
    model.save_weights("cifar10.hdf5")
    #Finally print the accuracy of our model!
    print("Accuracy: &2.f%%" %(model.evaluate(X_test, y_test)[1]*100))



#TCN  - Temporal Convolutional Network - Real Time Video
def is_power_of_two(num: int):
    return num != 0 and ((num & (num - 1)) == 0)


def adjust_dilations(dilations: list):
    if all([is_power_of_two(i) for i in dilations]):
        return dilations
    else:
        new_dilations = [2 ** i for i in dilations]
        return new_dilations


    

    def __init__(self,
                 dilation_rate: int,
                 nb_filters: int,
                 kernel_size: int,
                 padding: str,
                 activation: str = 'relu',
                 dropout_rate: float = 0,
                 kernel_initializer: str = 'he_normal',
                 use_batch_norm: bool = False,
                 use_layer_norm: bool = False,
                 use_weight_norm: bool = False,
                 **kwargs):

        self.dilation_rate = dilation_rate
        self.nb_filters = nb_filters
        self.kernel_size = kernel_size
        self.padding = padding
        self.activation = activation
        self.dropout_rate = dropout_rate
        self.use_batch_norm = use_batch_norm
        self.use_layer_norm = use_layer_norm
        self.use_weight_norm = use_weight_norm
        self.kernel_initializer = kernel_initializer
        self.layers = []
        self.shape_match_conv = None
        self.res_output_shape = None
        self.final_activation = None

        super(ResidualBlock, self).__init__(**kwargs)

    def tcn_full_summary(model: Model, expand_residual_blocks=True):
        #import tensorflow as tf
        # 2.6.0-rc1, 2.5.0...
        versions = [int(v) for v in tf.__version__.split('-')[0].split('.')]
        if versions[0] <= 2 and versions[1] < 5:
            layers = model._layers.copy()  # store existing layers
            model._layers.clear()  # clear layers

            for i in range(len(layers)):
                if isinstance(layers[i], TCN):
                    for layer in layers[i]._layers:
                        if not isinstance(layer, ResidualBlock):
                            if not hasattr(layer, '__iter__'):
                                model._layers.append(layer)
                        else:
                            if expand_residual_blocks:
                                for lyr in layer._layers:
                                    if not hasattr(lyr, '__iter__'):
                                        model._layers.append(lyr)
                            else:
                                model._layers.append(layer)
                else:
                    model._layers.append(layers[i])

            model.summary()  # print summary

            # restore original layers
            model._layers.clear()
            [model._layers.append(lyr) for lyr in layers]

            

        def _build_layer(self, layer):
           
            self.layers.append(layer)
            self.layers[-1].build(self.res_output_shape)
            self.res_output_shape = self.layers[-1].compute_output_shape(self.res_output_shape)

        def build(self, input_shape):

            with K.name_scope(self.name):  # name scope used to make sure weights get unique names
                self.layers = []
                self.res_output_shape = input_shape

                for k in range(2):  # dilated conv block.
                    name = 'conv1D_{}'.format(k)
                    with K.name_scope(name):  # name scope used to make sure weights get unique names
                        conv = Conv1D(
                            filters=self.nb_filters,
                            kernel_size=self.kernel_size,
                            dilation_rate=self.dilation_rate,
                            padding=self.padding,
                            name=name,
                            kernel_initializer=self.kernel_initializer
                        )
                        if self.use_weight_norm:
                            from tensorflow_addons.layers import WeightNormalization
                            # wrap it. WeightNormalization API is different than BatchNormalization or LayerNormalization.
                            with K.name_scope('norm_{}'.format(k)):
                                conv = WeightNormalization(conv)
                        self._build_layer(conv)

                    with K.name_scope('norm_{}'.format(k)):
                        if self.use_batch_norm:
                            self._build_layer(BatchNormalization())
                        elif self.use_layer_norm:
                            self._build_layer(LayerNormalization())
                        elif self.use_weight_norm:
                            pass  # done above.

                    with K.name_scope('act_and_dropout_{}'.format(k)):
                        self._build_layer(Activation(self.activation, name='Act_Conv1D_{}'.format(k)))
                        self._build_layer(SpatialDropout1D(rate=self.dropout_rate, name='SDropout_{}'.format(k)))

                if self.nb_filters != input_shape[-1]:
                    # 1x1 conv to match the shapes (channel dimension).
                    name = 'matching_conv1D'
                    with K.name_scope(name):
                        # make and build this layer separately because it directly uses input_shape.
                        # 1x1 conv.
                        self.shape_match_conv = Conv1D(
                            filters=self.nb_filters,
                            kernel_size=1,
                            padding='same',
                            name=name,
                            kernel_initializer=self.kernel_initializer
                        )
                else:
                    name = 'matching_identity'
                    self.shape_match_conv = Lambda(lambda x: x, name=name)

                with K.name_scope(name):
                    self.shape_match_conv.build(input_shape)
                    self.res_output_shape = self.shape_match_conv.compute_output_shape(input_shape)

                self._build_layer(Activation(self.activation, name='Act_Conv_Blocks'))
                self.final_activation = Activation(self.activation, name='Act_Res_Block')
                self.final_activation.build(self.res_output_shape)  # probably isn't necessary

                # this is done to force Keras to add the layers in the list to self._layers
                for layer in self.layers:
                    self.__setattr__(layer.name, layer)
                self.__setattr__(self.shape_match_conv.name, self.shape_match_conv)
                self.__setattr__(self.final_activation.name, self.final_activation)

                super(ResidualBlock, self).build(input_shape)  # done to make sure self.built is set True

        def call(self, inputs, training=None, **kwargs):
            """
            Returns: A tuple where the first element is the residual model tensor, and the second
                     is the skip connection tensor.
            """
            
            x1 = inputs
            for layer in self.layers:
                training_flag = 'training' in dict(inspect.signature(layer.call).parameters)
                x1 = layer(x1, training=training) if training_flag else layer(x1)
            x2 = self.shape_match_conv(inputs)
            x1_x2 = self.final_activation(layers.add([x2, x1], name='Add_Res'))
            return [x1_x2, x1]

        def compute_output_shape(self, input_shape):
            return [self.res_output_shape, self.res_output_shape]




        
@app.route('/pro44', methods=['GET', 'POST'])
def pro44():
    msg=""
    dimg=[]
    path_main = 'static/vehicle'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #####
        image = cv2.imread("static/vehicle/"+fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/trained/ff/"+fname
        #edged.save(path4)
        ##
    
    path_main = 'static/vehicle'
    for fname in os.listdir(path_main):
        
        parser = argparse.ArgumentParser(
        description='Script to run Yolo-V8 object detection network ')
        parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
        parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
                                          help='Path to text network file: '
                                               'MobileNetSSD_deploy.prototxt for Caffe model or '
                                               )
        parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
                                         help='Path to weights: '
                                              'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                              )
        parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
        args = parser.parse_args()

        # Labels of Network.
        classNames = { 0: 'background',
            1: 'plant' }

        # Open video file or capture device. 
        '''if args.video:
            cap = cv2.VideoCapture(args.video)
        else:
            cap = cv2.VideoCapture(0)'''

        #Load the Caffe model 
        net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

        #while True:
        # Capture frame-by-frame
        #ret, frame = cap.read()
        
        frame = cv2.imread("static/vehicle/"+fname)
        frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 400), (127.5, 127.5, 127.5), False)
        #Set to network the input blob 
        net.setInput(blob)
        #Prediction of network
        detections = net.forward()

        #Size of frame resize (300x400)
        cols = frame_resized.shape[1] 
        rows = frame_resized.shape[0]

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2] #Confidence of prediction 
            if confidence > args.thr: # Filter prediction 
                class_id = int(detections[0, 0, i, 1]) # Class label

                # Object location 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)
                
                # Factor for scale to original size of frame
                heightFactor = frame.shape[0]/300.0  
                widthFactor = frame.shape[1]/300.0 
                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom) 
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)
                # Draw location of object  
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                              (0, 255, 0))
                try:
                    y=yLeftBottom
                    h=yRightTop-y
                    x=xLeftBottom
                    w=xRightTop-x
                    image = cv2.imread("static/vehicle/"+fname)
                    mm=cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.imwrite("static/process1/"+fname, mm)
                    cropped = image[yLeftBottom:yRightTop, xLeftBottom:xRightTop]

                    #gg="segment.jpg"
                    #cv2.imwrite("static/result/"+gg, cropped)


                    #mm2 = PIL.Image.open('static/trained/'+gg)
                    #rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
                    #rz.save('static/trained/'+gg)
                except:
                    print("none")
                    #shutil.copy('getimg.jpg', 'static/trained/test.jpg')
                # Draw label and confidence of prediction in frame resized
                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    claname=classNames[class_id]

                    
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                         (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                         (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                    #print(label) #print class and confidence  
    return render_template('pro44.html',dimg=dimg)



@app.route('/upload',methods=['POST','GET'])
def upload():
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()
    fnn=""
    #if 'username' in session:
    #    uname = session['username']
    if request.method == 'POST':
        file = request.files['file']
        fnn=file.filename

        ff11=open("video.txt","w")
        ff11.write(fnn)
        ff11.close()

        
        file.save(os.path.join("static/upload", fnn))
        msg="success"

    return render_template('upload.html',msg=msg,title=title)

@app.route('/view_video',methods=['POST','GET'])
def view_video():
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()
    

    return render_template('view_video.html',msg=msg,title=title)


@app.route('/vehicle', methods=['POST','GET'])
def vehicle():
    msg=""
    ff11=open("title.txt","r")
    title=ff11.read()
    ff11.close()

    ff11=open("title1.txt","r")
    title1=ff11.read()
    ff11.close()

    ff11=open("title2.txt","r")
    title2=ff11.read()
    ff11.close()

    ff=open("static/amno.txt","w")
    ff.write("")
    ff.close()
    
    
    if request.method == 'POST':
        vno = request.form['vno']

        mycursor = mydb.cursor()

        utype='admin'
        mycursor.execute("SELECT count(*) FROM ap_register where vno=%s",(vno,))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            mycursor.execute("SELECT id FROM ap_register where vno=%s",(vno,))
            vid = mycursor.fetchone()[0]
            ff1=open("un.txt","w")
            ff1.write(vno)
            ff1.close()
            result=" Your Logged in sucessfully**"
            return redirect(url_for('vehicle_move',vid=vid)) 
        else:
            result="You are logged in fail!!!"

    
    
    return render_template('vehicle.html',msg=msg,title=title,title1=title1,title2=title2)






@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))

def gen(camera):

    while True:
        frame = camera.get_frame()
    

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    
@app.route('/video_feed')
def video_feed():
    
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
