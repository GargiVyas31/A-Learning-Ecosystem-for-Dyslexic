# -*- coding: utf-8 -*-
"""
It Normalizes the obj files
"""
import sys
import subprocess
def lines(fp):
    v_lines=[]
    f_lines=[]
    u_lines=dict()
    m_lines=[]
    fp.seek(0)
    all_lines=fp.readlines()
    for i in range(len(all_lines)):
        if all_lines[i][0]=="m":
            m_lines.append(all_lines[i])
        if all_lines[i][0]=="u":
            u_lines[i]=all_lines[i]
        if all_lines[i][0]=="v":   #Vertex data found
            v_lines.append(all_lines[i])
        if all_lines[i][0]=="f":  #Face data found
            f_lines.append(all_lines[i])
    return all_lines,v_lines,f_lines,u_lines,m_lines

def get_v(v_lines):
    v_x=[]
    v_y=[]
    v_z=[]
    for i in range(len(v_lines)):
        v_lines[i]=v_lines[i].rstrip('\n').lstrip('v ')
    v_x=list(map(lambda x:float(x.split()[0]),v_lines)) 
    v_y=list(map(lambda x:float(x.split()[1]),v_lines)) 
    v_z=list(map(lambda x:float(x.split()[2]),v_lines)) 
    check(0,v_lines,v_x)
    check(1,v_lines,v_y)
    check(2,v_lines,v_z)
    return v_x,v_y,v_z
    
def check(i,v_lines,v):
    for j in range(len(v_lines)):
        if v[j]!=float(v_lines[j].split()[i]) or len(v)!=len(v_lines):
            raise   ZeroDivisionError
            
def normalize(v):
    avg=sum(v)/len(v)
    for i in range(len(v)):
        v[i]-=avg
        
def write_file(v_x,v_y,v_z,f_lines,m_lines,u_lines,fw):
    ctr=0
    for i in range(len(m_lines)):
        fw.write(m_lines[i])
    for i in range(len(v_x)):
        fw.write("v" + " " + str(v_x[i]) + " " + str(v_y[i]) + " " + str(v_z[i]) + '\n')
    for j in range(len(f_lines)):
        t_line=len(m_lines)+len(v_x)+j+ctr
#        print(t_line)
        if t_line in u_lines:
            fw.write(u_lines[t_line])
            ctr+=1
        fw.write(f_lines[j])
        
def main_2(s):
    fp=open(s,"r")
    n="normalized_"+s
    ft=open(n,"w")
    all_lines,v_lines,f_lines,u_lines,m_lines=lines(fp)
    v_x,v_y,v_z=get_v(v_lines)
    normalize(v_x)
    normalize(v_y)
    normalize(v_z)
    write_file(v_x,v_y,v_z,f_lines,m_lines,u_lines,ft)
    fp.close()
    ft.close()
    return n
def main():
    files_made=[]
    for i in sys.argv[1:]:
        files_made.append(main_2(i))
    if len(files_made)!=0:
        print("Stage--2 Passed")
        print(sys.argv)
        #subprocess.call(['rm',sys.argv[1],sys.argv[2]],shell=True)
        subprocess.call(['python','Models/3_Modifying.py',files_made[0],files_made[1]])
    else:
        print("not found")
        raise FileNotFoundError
main()