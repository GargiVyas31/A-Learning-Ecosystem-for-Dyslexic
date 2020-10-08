# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 09:58:19 2018

@author: kansa

It places the object on top
"""

fp1=open("Test1.obj","r")
fp2=open("Test2.obj","r")
v_list=[]
f_list=[]
m_lines=[]
m2_lines=[]
u_lines=dict()
u2_lines=dict()
v2_list=[]
f2_list=[]
s2=fp2.readlines()
for i in range(len(s2)):
    try:
        if s2[i][0]=="u":
            u2_lines[i]=s2[i]
        if s2[i][0]=="m":
            m2_lines.append(s2[i])
        if s2[i][0]=="v":
            s2[i]=s2[i].rstrip('\n')
            v2_list.append(list(map(float,s2[i].split()[1:])))
        if s2[i][0]=="f":
            f2_list.append(s2[i])
    except ValueError:
        print(i)
        

max=0
for i in range(len(v2_list)):
    val=v2_list[i][2]
    if val>max:
        max=val
        
for i in range(len(v2_list)):
        if max>0:
            v2_list[i][2]-=abs(max)
        if max<0:
            v2_list[i][2]+=abs(max)
            

max=0
for i in range(len(v2_list)):
    val=v2_list[i][2]
    if val>max:
        max=val

s=fp1.readlines()
"""
for i in range(len(s)):
    if s[i][0]=="v":
        s[i]=s[i].rstrip('\n')
        v_list.append(list(map(float,s[i].split()[1:])))
    if s[i][0]=="f":
        f_list.append(s[i])
"""
for i in range(len(s)):
    try:
        if s[i][0]=="u":
            u_lines[i]=s[i]
        if s[i][0]=="m":
            m_lines.append(s[i])
        if s[i][0]=="v":
            s[i]=s[i].rstrip('\n')
            v_list.append(list(map(float,s[i].split()[1:])))
        if s[i][0]=="f":
            f_list.append(s[i])
    except ValueError:
        print(i)

min=0
for i in range(len(v_list)):
    val=v_list[i][2]
    if val<min:
        min=val

for i in range(len(v_list)):  
        if min>0:
            v_list[i][2]-=abs(min)
        if min<0:
            v_list[i][2]+=abs(min)


fw1=open("11.obj","w")
fw2=open("22.obj","w")

w(v_list,m_lines,fw1)
w(v2_list,m2_lines,fw2)
f(f_list,v_list,m_lines,u_lines,fw1)
f(f2_list,v2_list,m2_lines,u2_lines,fw2)
fw1.close()
fw2.close()    
fp1.close()
fp2.close()
