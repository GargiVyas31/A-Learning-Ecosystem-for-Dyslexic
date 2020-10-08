"""
It removes unrequired things
""" 
import sys
import subprocess
def createfile(ft,s):
    for i in s:
        try:
            if i[0:2]=="v ":
    #            print(i +'\n')
                ft.write(i +'\n')
            if i[0]=="u":
    #            print(i +'\n')
                ft.write(i +'\n')
            if i[0]=="f":
                line=i.split()
                line=line[1:]
                newline=[]
                for j in range(len(line)):
                    newline.append(line[j].split('/')[0])
                f="f "+newline[0]+" "+newline[1]+" "+newline[2]+"\n"
                ft.write(f)
    #            print(f)
            if i[0]=="m":
                ft.write(i+'\n')        
        except IndexError:
            pass
#            print("line is",i)
            
    
def close(fp,ft):
    fp.close()
    ft.close()
    
def main():
    print("Object Creation Initialized")
    files_made=[]
    for i in sys.argv[1:]:
        fp=open(i,"r")
        name="prep_"+i
        ft=open(name,"w")
        s=fp.read().split('\n')
        createfile(ft,s)
        close(fp,ft)
        files_made.append(name)
    if len(files_made)!=0:
        print('Stage 1-Passed')
        subprocess.call(['python','2_Normalization.py',files_made[0],files_made[1]])
    else:
        raise FileNotFoundError
    
main()
