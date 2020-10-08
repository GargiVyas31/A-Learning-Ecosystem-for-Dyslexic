# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 11:58:23 2018

@author: kansa
"""
import sys
import subprocess

def gather(f):
    v_list=[]
    f_list=[]
    m_list=[]
    u_list=dict()
    s=f.readlines()
    for i in range(len(s)):
        try:
            if s[i][0]=="m":
                m_list.append(s[i])
            elif s[i][0]=="v":
                v_list.append(list(map(float,(s[i].rstrip('\n')).split()[1:])))
            elif s[i][0]=="u":
                u_list[i]=s[i]         
            elif s[i][0]=="f":
                f_list.append(s[i])
        except ValueError:
            pass
    return v_list,f_list,m_list,u_list


def perform(v,func,index):
    m=0
    for i in range(len(v)):
        val=v[i][index]
        if func==max:
            if val>m:
                m=val
        elif func==min:
            if val<m:
                m=val
    for i in range(len(v)):
            if m>0:
                v[i][index]-=abs(m)
            if m<0:
                v[i][index]+=abs(m)
def write_v(v,m,fp):
    for i in m:
        fp.write(i)
    for i in range(len(v)):
        fp. write("v " + str(v[i][0])+" "+ str(v[i][1])+" "+ str(v[i][2])+"\n")
        
def write_f(f,v,m,u,fp):
    ctr=0
    for i in range(len(f)):
        t_line=len(v)+len(m)+i+ctr
        if t_line in u:
            fp.write(u[t_line])
            ctr+=1
        fp.write(f[i])
        
def close(fp,ft):
    fp.close()
    ft.close()
            
def main_2(s,func):
    fp=open(s,'r')
    n="placed_"+s
    ft=open(n,'w')
    v,f,m,u=gather(fp)
    perform(v,func,2) # x=0 y=1 z=2
    write_v(v,m,ft)
    write_f(f,v,m,u,ft)
    close(fp,ft)
    return n
def main():
    files_made=[]
    files_made.append(main_2(sys.argv[1],max))
    files_made.append(main_2(sys.argv[2],min))
    if len(files_made)!=0:
        print('Stage-3 Passes')
        subprocess.call(['del',sys.argv[1],sys.argv[2]],shell=True)
        subprocess.call(['python','4_Combining.py',files_made[0],files_made[1]])
    else:
        raise FileNotFoundError
main() 
    
    
    