 # -*- coding: utf-8 -*-

import re
import pandas as pd

#normal(neg)=0 attack(pos)=1
#from leftobspatternV import primepatterns



df = pd.read_csv(r'Iot-train-50k-bin.csv').dropna()   #after dropping duplicates from the gainratio file
#df = pd.read_csv(r'C:\Users\NITUK\Dropbox\lad\final lad code\checked  result\final code lad\Support-mtech.csv')
#df = pd.read_csv(r'C:\Users\NITUK\Dropbox\lad\final lad code\checked  result\new idea lad\NUM_supportset-trial.csv')
#df = pd.read_excel(r'C:\Users\user\Dropbox\lad\pattern\input1.xlsx')
#df  = pd.read_csv(r'C:\Users\NITUK\Dropbox\mtech student\lad output\updated_support_set.csv')
#df = pd.read_csv(r'E:\OneDrive - iitr.ac.in\lad\Lad paper info gain 5 aug 2021\supportset-infogain.csv')
col_name = "result" #input("enter result column name")
# df.drop(df.iloc[:, 51:661], inplace = True, axis = 1)
df = df.sort_values(col_name,ascending=False)
df = df.reset_index(drop=True)
print(df)

P = []          #PATTERNS GENERATED
#D=3
c=[[]]          #CANDIDATE TERMS
p=0     #maximum index of the literal in  T
D = 4 #maximum degree of the generated patterns                                                                                                                                                                                                                              #DEGREE OF GENERATED PATTERN - NO OF LITERALS
n = 59  #no of input variables (features)
f=1
x=0
z=0
out_list=[]   #for storing result column
list_col = df.values.T.tolist()
del_row =[]  # index of row to be deleted once used to check positive pattern
#print(list_col)
x = 60 #int(input("enter col no having output"))
out_list = list_col[x-1]
#print("out_list",out_list)
pos=0           #no. of positive observations
neg=0           #no. of negative observations
for i in out_list:
    if(i==1):
        pos=pos+1
    else:
        neg=neg+1
print("pos =",pos," neg=", neg)

df_old=df
print(df_old)

for d in range(1,D+1):          #loop from 1 to D 
    
    #print("FIRST FOR ",d)
    #print(d,"   ",c[d-1])         #print previous candidate terms
    if(d<D):
        c.append([])
        #print("C = ",c)
        #print(c)
    if(len(c[d-1])==0):
        print("in first if")
        t1=[]
        for s in range(p+1,n+1):
                #print("THIRD FOR ",s)
                l =[s,-s]
                #print("l = ",l)   
                t2 = []
                for ln in l:
                    #print("FOURTH FOR ",ln)
                    t2=t1.copy()
                    t2.append(ln)
                    #print("t2=",t2)
                    for i in range(1,d+1):
                        # print("FIFTH FOR ",i," d= ",d, "  t2 =  ",t2) #,"  t3 =   ",t3)
                        #t2.sort()
                        t3 =t2.copy()
                        #print("t3 and t2 =",t3,t2)
                        '''if(i in t3):
                            print("positive remove")
                            t3.remove(i)
                        elif(-i in t3):
                            print("negative remove")
                            t3.remove(-i)
                        elif(len(t3)==1):
                            t3.pop(0)
                            print("after pop",t3)'''
                        t3.pop(i-1)
                        #print("t3 and t2=",t3,t2)
                        #print("c[d-1]",c[d-1])
                        if(t3 == c[d-1]):
                            #print("continue",t3,c[d-1])
                            continue
                        else:
                            #print("not continue")
                            f=0
                            break
                    if(f==1):
                        #print("hello")
                        #print("len=0",t2)
                        #print(df)
                        #list_col = df.values.T.tolist()
                        #print("value of df =",list_col)
                        for t in t2:
                            #print("t=",t)
                            if(t<0):
                                z=1
                                t=-t
                            for col in range(len(df.columns)):
                                #print("col = ",col)
                                '''if(col==x):
                                    break'''
                                if(col==t):
                                    #global list_col
                                    #print("true"," col = ",col)
                                    list_c = list_col[col-1]
                                    if(z==1):
                                        list_newc =[]
                                        for y in list_c:
                                            y = 1-y
                                            list_newc.append(y)
                                        list_c=list_newc.copy()
                                    z=0
                                    # print("value =",list_c)
                                    flag_p=0
                                    flag_n=0
                                    #print("pos = ",pos, "neg = ",neg, "  ",len(list_col[col-1]))
                                    for k in range(len(list_c)-neg):
                                        
                                        if(list_c[k]>0):
                                            flag_p = flag_p +1
                                            
                                            del_row.append(k)
                                    # print(s,"flag_p=",flag_p)
                                    if(flag_p>=1):
                                        #k=3
                                        for k in range(pos,len(list_c)):
                                            if(list_c[k]>0):
                                                flag_n = flag_n +1
                                        #print("flag_n=",flag_n)
                                        if(flag_n<1):
                                            #print("pattern")
                                            P.append(t2)
                                            q=0
                                            #counter=0
                                            while(len(del_row)>q):
                                                df = df.drop(del_row[q])
                                                q = q+1
                                                #counter+1
                                            #print(df1)
                                            df =df.reset_index(drop=True)
                                            #print("df -1",df)
                                            
                                            #print("hello")
                                            list_col = df.values.T.tolist()
                                            
                                            out_list = list_col[x-1]
                                            #global pos
                                            pos=0
                                            #global neg
                                            neg=0
                                            for i in out_list:
                                                if(i==1):
                                                    pos=pos+1
                                                else:
                                                    neg=neg+1
                                            print(flag_p,"pos = ", pos, "   neg = ", neg)
                                        elif(d<D):
                                            c[d].append(t2)
                                            #print("C[d] = ",c[d])
                                        #print("P = ",P)
                                    del_row=[]    #print("C[d] = ",c[d])
                                    break
                    

    if(len(c[d-1])!=0):
        #print("len>1")
        for t1 in c[d-1]:
            #print("Second FOR \n t1= ",t1)
            #print("t1=",t1)
            #t1.sort(reverse=True)
            if(len(t1)==0):
                p=0
            else:
                p = t1[len(t1)-1]
                if(p<0):
                    p=-p
            #print("in p",p)
            #print(p)
            for s in range(p+1,n+1):
                #print("THIRD FOR ",s)
                l =[s,-s]
                #print("l = ",l)
                t2 = []
                for ln in l:
                    #print("FOURTH FOR ",ln)
                    #print("t1 before copy",t1)
                    t2=t1.copy()
                    t2.append(ln)
                    #print("t2=",t2)
                    for i in range(1,d+1):
                        #print("FIFTH FOR ",i)
                        #t2.sort()
                        t3 =t2.copy()
                        #print("t3 and t2 =",t3,t2)
                        '''if(i in t3):
                            print("positive remove")
                            t3.remove(i)
                        elif(-i in t3):
                            print("negative remove")
                            t3.remove(-i)
                        elif(len(t3)==1):
                            t3.pop(0)
                            print("after pop",t3)'''
                        t3.pop(i-1)
                        #print("t3 and t2 =",t3,t2)
                        #print("c[d-1]",c[d-1])
                        if(t3 in c[d-1]):
                            #print("continue",t3,c[d-1])
                            f=1
                            continue
                        else:
                            #print("not cotiniue")
                            f=0
                            break
                    if(f==1):
                        # print("hello")
                        #print("len<1",t2)
                        #print(df)
                        #list_col = df.values.T.tolist()
                        #print("value of df =",list_col)
                        if(len(t2)<1):
                            for t in t2:
                                #print("t=",t)
                                if(t<0):
                                    z=1
                                    t=-t
                                for col in range(len(df.columns)):
                                    #print("col = ",col)
                                    '''if(col==x):
                                        break'''
                                    if(col==t):
                                        #global list_col
                                        #print("true","col = ",col)
                                        list_c = list_col[col-1]
                                        if(z==1):
                                            list_newc =[]
                                            for y in list_c:
                                                y = 1-y
                                                list_newc.append(y)
                                            list_c=list_newc.copy()
                                        z=0
                                        #print("value =",list_c)
                                        flag_p=0
                                        flag_n=0
                                        #print("before", pos, neg)
                                        #print("pos = ",pos, "neg = ",neg, "  ",len(list_col[col-1]))
                                        for k in range(len(list_c)-neg):
                                            if(list_c[k]>0):
                                                flag_p = flag_p +1
                                                del_row.append(k)
                                        if(flag_p>=1):
                                            #k=3
                                            for k in range(pos,len(list_c)):
                                                if(list_c[k]>0):
                                                    flag_n = flag_n +1
                                            if(flag_n<1):
                                                P.append(t2)
                                                q=0
                                                #counter=0
                                                while(len(del_row)>q):
                                                    df = df.drop(del_row[q])
                                                    q = q+1
                                                    #counter+1
                                                #print(df1)
                                                df = df.reset_index(drop=True)
                                                
                                                list_col = df.values.T.tolist()
                                                out_list = list_col[x-1]
                                                #global pos
                                                pos=0
                                                #global neg
                                                neg=0
                                                for i in out_list:
                                                    if(i==1):
                                                        pos=pos+1
                                                    else:
                                                        neg=neg+1
                                                #print("pos = ", pos, "   neg = ", neg)
                                                #print(del_row)
                                                print(flag_p,"pos = ", pos, "   neg = ", neg)
                                            elif(d<D):
                                                c[d].append(t2)
                                                #print("C[d] = ",c[d])
                                            #print("P = ",P)
                                        del_row=[]    

                                        break
                        if(len(t2)>1):
                            new_list=[]
                            list_f=[]
                            len_c=0
                            for t in t2:
                                #print("t=",t)
                                if(t<0):
                                    z=1
                                    t=-t
                                for col in range(len(df.columns)):
                                    #print("col = ",col)
                                    '''if(col==x):
                                        break'''
                                    if(col==t):
                                        #global list_col
                                        #print("true","col = ",col, t, df.columns[col-1])
                                        list_c = list_col[col-1]
                                        if(z==1):
                                            list_newc =[]
                                            for y in list_c:
                                                y = 1-y
                                                list_newc.append(y)
                                            list_c=list_newc.copy()
                                        z=0
                                        #print("value =",list_c)
                                        new_list.append(list_c)
                                        #print(new_list)
                                        len_c=len(list_c)
                                        break
                            len_new=len(new_list)
                            mul = 1
                            #print("new list",new_list)
                            #print("len_c",len_c)
                            #print("len  new list",len_new)
                            for j in range(len_c):
                                mul=1
                                for m in range(len_new):

                                    mul = mul and new_list[m][j]
                                list_f.append(mul)
                            #print(list_f)
                            flag_p=0
                            flag_n=0
                            #print("before", pos, neg)
                            #print("pos = ",pos, "neg = ",neg, "  ",len(list_col[col-1]))
                            for k in range(len(list_f)-neg): #-3 if false =3
                                if(list_f[k]>0):
                                    flag_p = flag_p +1
                                    del_row.append(k)
                            #print("flag_p=",flag_p)
                            if(flag_p>=1):
                                #k=3
                                for k in range(pos,len(list_f)):
                                    if(list_f[k]>0):
                                        flag_n = flag_n +1
                                #print("flag_n =",flag_n)
                                if(flag_n<1):
                                    P.append(t2)
                                    q=0
                                    #counter=0
                                    while(len(del_row)>q):
                                        #df= df1.copy()
                                        #df.reset_index()
                                        #print("after reset")
                                        #print(del_row[q])
                                        df = df.drop(del_row[q])
                                        
                                        q = q+1
                                        #counter+1
                                    #print(df)
                                    #print("after delete")
                                    #df=df1.copy()
                                    #print(df)
                                    df = df.reset_index(drop=True)
                                    #global list_col
                                    list_col = df.values.T.tolist()
                                    out_list = list_col[x-1]
                                    #global pos
                                    pos=0
                                    #global neg
                                    neg=0
                                    for i in out_list:
                                        if(i==1):
                                            pos=pos+1
                                        else:
                                            neg=neg+1
                                    print(flag_p,"pos = ", pos, "   neg = ", neg)
                                    #print(del_row)
                                    
                                elif(d<D):
                                    #print("about to append",c,d)
                                    c[d].append(t2)
                                    
                                    #print("C[d] = ",c[d])
                            del_row=[]    #print("P = ",P)
 
print(df)     
c=df.columns.tolist()             
list_col = df.values.tolist()
list_row =df.values.T.tolist()
out_list = list_row[x-1]
list_col1=list_col
print(len(list_col[0]))
df=pd.DataFrame(list_col1,columns=c)

list_col=list_row
print(len(list_col[0]))
pos=0
neg=0
for i in out_list:
    if(i==1):
        pos=pos+1
    else:
        neg=neg+1
print("pos = ", pos, "   neg = ", neg)

#df.to_csv("E:\OneDrive - iitr.ac.in\lad\Lad paper info gain 5 aug 2021\leftdata.csv",index=None)


#pp=primepatterns()
#pp.pg()

#PATTERNS GENERATED FROM REMAINING OBSERVATION TOP DOWN APPROACH

# pp=[]
# count_pp=[]
# counter =0
# for row in list_col:
#     new_p=[]
#     if(counter<pos):
#         for col in range(len(df.columns)):
#             if(col != 29):
                
#                 if(row[col]==1):
#                     new_p.append(col)
#         print(new_p)
#         for i in range(1,len(new_p)):
#             i=0
#             del(new_p[i])
#             print("  dsd" ,new_p)
#             new_list=[]
#             for i in new_p:
#                 new_list.append(list_row[i])
#             len_new = len(new_list)
#             len_c = len(new_list[0])
#             list_f=[]
#             for j in range(len_c):
#                 mul=1
#                 for m in range(len_new):
            
#                     mul = mul and new_list[m][j]
#                 list_f.append(mul)
#             #print(list_f)
#             flag_p=0
#             flag_n=0
#             #print("before", pos, neg)
#             print("pos = ",pos, "neg = ",neg, "  ",len(list_f), flag_p)
#             for k in range(len(list_f)-neg): #-3 if false =3
#                 if(list_f[k]>0):
#                     flag_p = flag_p +1
#                     del_row.append(k)
#             print("flag_p=",flag_p)
#             if(flag_p>30):
#                 #k=3
#                 for k in range(pos,len(list_f)):
#                     if(list_f[k]>0):
#                         flag_n = flag_n +1
#                 #print("flag_n =",flag_n)
#                 if(flag_n<30):
#                     pp.append(new_p)
#                     count_pp.append(flag_p)
#                     counter = counter +flag_p
#                     q=0
#                     #counter=0
#                     # while(len(del_row)>q):
#                     #     #df= df1.copy()
#                     #     #df.reset_index()
#                     #     #print("after reset")
#                     #     #print(del_row[q])
#                     #     df = df.drop(del_row[q])
                        
#                     #     q = q+1
#                     #     #counter+1
#                     # #print(df)
#                     # #print("after delete")
#                     # #df=df1.copy()
#                     # #print(df)
#                     # df = df.reset_index(drop=True)
#                     # #global list_col
#                     # list_col = df.values.tolist()
#                     # list_row =df.values.T.tolist()
#                     # out_list = list_row[x-1]
#                     # #global pos
#                     # pos=0
#                     # #global neg
#                     # neg=0
#                     # for i in out_list:
#                     #     if(i==1):
#                     #         pos=pos+1
#                     #     else:
#                     #         neg=neg+1
#                     # print(flag_p,"pos = ", pos, "   neg = ", neg)
#                 #print(del_row)
#     else:
#         break
        
# print(pp)   
# print(count_pp)
#print("c = ")
'''for d in range(1,D):
    print(d, "   ",c[d],"\n")'''
print("PATTERNS ARE : \n")
print("P = ", P)
print(len(P))
P1=P #first time patterns flagp>50
P2 = P #second time patterns flagp>1
df1=pd.read_csv(r'UNSW_2018_IoT_Botnet_Final_10_best_Training.csv')
col  =df1.columns
columns = df.columns
print(col)
pattern = []

for k in range(len(P)):
    term=[]
    for j in P[k]:
        #print(j)
        if(j>0):
            l = columns[j-1]
            
            for i in range(len(col)):
                if(re.search(col[i],l)):
                    print(col[i],l)
                    
                    l=l.replace(col[i],"col["+str(i)+"]")
                    l=l.replace("cp"," ")
                    if(re.search("<=",l) or re.search("<",l)):
                        print("no")
                    elif(re.search("=",l)):
                        l=l.replace("=",">=")
                    
                    #print(l)        
                    break
            
            term.append(l)
            
        else:
            g= -j
            s = columns[g-1]
            for i in range(len(col)):
                if(re.search(col[i],s)):
                    print(col[i],s)
                    
                    s=s.replace(col[i],"col["+str(i)+"]")
                    s=s.replace("cp"," ")
                    if(re.search("<=",s) or re.search("<",s)):
                        s="not("+s+")" 
                    elif(re.search("=",s)):
                        s=s.replace("=","<")
                    #print(l) 
                    break
            
            #print(s.capitalize())
            term.append(s)
            #\overline{columns[j-1]}
            
    print(term)
    pattern.append(term)
    
print(pattern)
print(len(pattern)) 
df2 = pd.DataFrame(data ={ "col2" : pattern})
print(df2)
y= "D:\\IDEAL 2023 work 13 sept\\Iot-50k-pattern-pos1.csv"
df2.to_csv(y,index=None)
# print(df)
# y= "D:\\OneDrive - iitr.ac.in\\PHD 29 July\\BOT-IOT Dataset work\\10-best Training-Testing split\\Iot-leftobs3.csv"
# df.to_csv(y,index=None)
# print(df)


'''
from csv import writer
from itertools import combinations
import numpy as np
import pandas as pd


class primepatterns():
    def __init__(self, k=1, D=3,obs_positive=50,obs_negative=50):
        self.k = k
        self.D = D
        self.obs_positive=obs_positive
        self.obs_negative=obs_negative
        self.__ppatterns = {}
        self.__npatterns = {}

    def pg(self,df):
        p = 0
        q = 0
        # df = pd.read_csv('support_set.csv', dtype='uint8')
        # print(df)
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1:]
        y = y.to_numpy()
        neg=-1
        while not X.empty and len(X)>=100:
            neg+=1
            print("starts")
            # self.obs_positive=self.obs_positive-300
            # self.obs_negative= self.obs_negative-100

            for d in range(1, self.D + 1):
                for literals in combinations(X, d):
                    literals = list(literals)
                    columns = X[literals]
                    columns = columns.to_numpy()
                    for unique_values in np.unique(columns, axis=0):
                        # print("x intial")
                        # print(X)
                        covered = []
                        counts = 0
                        for instance in columns:
                            if (unique_values == instance).all():
                                covered.append(counts)
                                counts += 1
                            else:
                                counts += 1
                        _labels = np.unique(y[covered])
                        unique, counts = np.unique(y[covered], return_counts=True)
                        label = {unique[i]: counts[i] for i in range(len(unique))}
                        # print("len(covered)")
                        # print(len(covered))
                        # print( unique, counts)
                        # print(unique_values)
                        if (_labels.all() == 1 and len(covered) > self.obs_positive) or (
                                len(_labels) == 2 and len(covered) > self.obs_positive and counts[0] <= 10):
                            self.__ppatterns[q] = literals, list(unique_values)
                            # print("len(covered)  positive patterns")
                            # print(_labels)
                            # print(unique, counts)
                            # print(len(covered))
                            # print(literals, list(unique_values))
                            # print(self.__ppatterns)
                            q += 1
                            X = X.drop(covered, axis=0)
                            X = X.reset_index(drop=True)
                            columns = np.delete(columns, covered, axis=0)
                            y = np.delete(y, covered, axis=0)
                            # print(covered)
                            # print(X)
                            # print(columns.shape)
                            # print(y.shape)
                            # elif (_labels.all() != 1 and len(_labels) == 1 and len(covered) > 30) or (
                            # len(_labels) == 2 and len(covered) > 50 and counts[1] <= 0):
                        elif _labels.all() != 1 and len(_labels) == 1 and len(covered) >  self.obs_negative:
                            self.__npatterns[p] = literals, list(unique_values)
                            # print("len(covered) negative patterns")
                            # print(_labels)
                            # print(unique, counts)
                            # print(len(covered))
                            # print(literals, list(unique_values))
                            # print(self.__npatterns)
                            p += 1
                            X = X.drop(covered, axis=0)
                            X = X.reset_index(drop=True)
                            columns = np.delete(columns, covered, axis=0)
                            y = np.delete(y, covered, axis=0)
                            # print(covered)
                            # print(X)
                            # print(columns.shape)
                            # print(y.shape)
                        # print("yshape")
                        # print(y.shape)
                        X = X

        # print("X")
        # print(X)
        # print("positive")
        # print(self.__ppatterns)
        # print("negative")
        # print(self.__npatterns)
        # print(len(self.__ppatterns))
        # print(len(self.__npatterns))
        # print(X.info())
        # print(y)
        if len(self.__ppatterns) != 0:
            with open('positive.csv', 'w') as f1:
                for key in self.__ppatterns.keys():
                    f1.write("%s,%s\n" % (key, self.__ppatterns[key]))
        if len(self.__npatterns) != 0:
            with open('negative.csv', 'w') as f2:
                for key in self.__npatterns.keys():
                    f2.write("%s,%s\n" % (key, self.__npatterns[key]))







pp=primepatterns()
pp.pg(df)

'''


























'''
for i in pattern:
    print(i)
    print(" ")

p1=[]
p2=[]         
for j in pattern:
    print(j)
    if(len(j)==2):
        p1.append(j)
    else:
        p2.append(j)        

print(p1)
print(p2)
df1 = pd.DataFrame(data = {"col1": p1})
df2 = pd.DataFrame(data ={ "col2" : p2})

print(df1)
print(df2)
y= input("enter output file path")
df1.to_csv(y,index=None)

y= input("enter output file path")
df2.to_csv(y,index=None)





'''



'''if(len(t2)>1):
    new_list=[]
    list_f=[]
    len_c=0
    for t in t2:
        print("t=",t)
        if(t<0):
            x=1
            t=-t
        for col in df:
            print("col = ",col)
            if(col==4):
                break
            if(col==t):
                print("true")
                list_c = list_col[col-1]
                if(x==1):
                    list_newc =[]
                    for y in list_c:
                        y = 1-y
                        list_newc.append(y)
                    list_c=list_newc.copy()
                x=0
                print("value =",list_c)
                new_list.append(list_c)
                len_c=len(list_c)
        len_new=len(new_list)
        mul = 1
        for j in range(len_c):
            for m in range(len_new):
                print(new_list[m][j])
                mul = mul and new_list[m][j]
            list_f.append(mul)

    flag_p=0
    flag_n=0
    for k in range(len(list_f)-3):
        if(list_f[k]>0):
            flag_p = flag_p +1
    if(flag_p>0):
        k=3
        for k in range(3,len(list_f)):
            if(list_f[k]>0):
                flag_n = flag_n +1
        if(flag_n<1):
            P.append(t2)
        else:
            c[d].append(t2)
        print("P = ",P)
        print("C[d] = ",c[d])'''

