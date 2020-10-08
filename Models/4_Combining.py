# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 11:25:40 2018

@author: kansa
"""
import sys
import subprocess

def func(f1,f2):
    fp1=open(f1,"r")
    print("opened f1")
    fp2=open(f2,"r")
    print("opened f1")
    fw=open('combined'+f1+f2, 'w')
    fm1=open(f1[23:][:-4]+".mtl","r")
    fm2=open(f2[23:][:-4]+".mtl","r")
    s1=fm1.read()
    s2=fm2.read()
    fm1.close()
    fm2.close()
    l1=fp1.readlines()
    l2=fp2.readlines()
    u_values=[]
    l1_new=list(map(lambda x: x.rstrip('\n'),l1))
    max_f=int(l1_new[-2].split()[-1])
#    fw.write(l1[0])
    fw.write("mtllib " + f1+f2+".mtl"+'\n')
    for i in range(1,len(l1)):
        if l1[i][0]!="f" and l1[i][0]!="u" :
            fw.write(l1[i])
    fw.write("\n#V of 1 done\n")    
    for j in range(1,len(l2)):
        if l2[j][0]!="f" and l2[j][0]!="u":
            fw.write(l2[j])
    fw.write("\n#V of 2 done\n")  
    for i in range(len(l1)):
        if l1[i][0]=="f" or l1[i][0]=="u":
            if l1[i][0]=="u":
               u_values.append(l1[i].rstrip('\n')[-1]) 
            fw.write(l1[i])
    
    max_u=max(list(map(lambda x:int(x),u_values)))
    for i in range(len(l2)):
        try:
            if l2[i][0]=="f":
                l2[i]=l2[i].split()
#                print(l2[i])
                l2[i]=list(map(lambda x:int(x)+max_f,l2[i][1:]))
#                print(l2[i])
                fw.write("f "+str(l2[i][0])+" "+str(l2[i][1])+ " "+str(l2[i][2])+"\n")
            elif l2[i][0]=="u":
                cu_line=l2[i]
                cu_line=cu_line.split()
                new_val=str(int(cu_line[1][1:])+max_u+1)
                fw.write("usemtl" + " "+ "m"+new_val+'\n')
        except ValueError:
            pass
    fmw=open(f1+f2+".mtl","w")
    fmw.write(s1)
    s2=s2.split('\n\n')
    final=""
    for i in range(len(s2)):
        strw=""
        if s2[i][:8]=="newmtl m":
            sp=s2[i].split('\n')
            number=float(sp[0][8:])
            add_val=number+max_u
            sp[0]="newmtl m"+str(add_val)
            for j in sp:
                strw+=j+'\n'
            final+=strw +'\n'
        else:
            final+=s2[i]+'\n\n'
    close(fp1,fp2,fw,fmw)
    
def main():
    func(sys.argv[1],sys.argv[2])
    print("Stage-4 Passed")
    #subprocess.call(['rm',sys.argv[1],sys.argv[2]],shell=True)
    print("Object Successfully Created")

def close(fp1,fp2,fw,fmw):        
    fp1.close()
    fp2.close()
    fw.close()
    fmw.close()
main()