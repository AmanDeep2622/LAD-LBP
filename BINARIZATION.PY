# -*- coding: utf-8 -*-
"""

@author: Sneha

Date : 10 july 2020
"""
import pandas as pd
import gc
# from sklearn.model_selection import train_test_split

# FUNCTION NUM
def num(df):
    result_col = "attack" #input("enter name of result column")
    all_cutpoints=[]
    original_df=df.copy()
    count_cutpoint = 0
    for col in df:
        
        collst=[]
        collst.append(col)
        collst.append(result_col)
        if col!=result_col:
            
            cutpoints=[]
            
            df_short = pd.DataFrame(df,columns = collst)
            
            df_short.sort_values(col,ascending=False,inplace=True)
            temp=df_short[[col,result_col]].values.T.tolist()
            
            # CHANGE LABEL IF SAME OBSERVATION HAS DIFFERENT LABEL
            for i in range(len(temp[0])-1):
                if(temp[0][i]==temp[0][i+1])and(temp[1][i]!=temp[1][i+1]):
                    c=max(temp[1])+1
                    temp[1][i]=c
                    temp[1][i+1]=c
            
            #CUTPOINT CALCULATION 
            for i in range(len(temp[0])-1):
                if(temp[0][i]!=temp[0][i+1])and(temp[1][i]!=temp[1][i+1]):
                    cutpoints.append((temp[0][i] + temp[0][i+1])/2)
            
            all_cutpoints.append(cutpoints)
            print(len(cutpoints))
            count_cutpoint = count_cutpoint + len(cutpoints)
            
    # print("ALL CUTPOINTS",all_cutpoints)
    
    
    #BINARIZATION
    result_list=original_df[result_col].tolist()
    df1=original_df.drop(columns=result_col) #drop label column
    
    temp=df1.values.T.tolist()
    col_names = df1.columns
    
    del df1
    del original_df
    gc.collect()
    print("TEMP WITHOUT LABEL")
    
    all_bin=[]
    lst=[]
    #t=0
    #count_cutpoint = 0
    ctr = 0  #counter for column name
    for l in all_cutpoints:
        #count_cutpoint = count_cutpoint + len(l)
        if(len(l)<175):
            #count_cutpoint = count_cutpoint + len(l)
            for i in l:
                lst.append(col_names[ctr] + "cp =" + str(i))  #put column name also
                bin_d=[]
                for j in temp[ctr]:
                    if(j>i):
                        bin_d.append(1)
                    else:
                        bin_d.append(0)
                    
           
                all_bin.append(bin_d)
        #t=t+1
        else:
            print(col_names[ctr],"  ",len(l))
        ctr = ctr +1
    print("LIST HEAD CP = ",len(lst))
    
    
    level_df = pd.DataFrame(all_bin)
    level_df = level_df.transpose()
    level_df.columns=lst
    #print("LEVEL DF")
    
    print("total cutpoints  = ",count_cutpoint)
    
#     ctr=0
#     lst_cp=[]
#     all_interval_bin=[]
#      #cp_pairs=[]
#     for l in all_cutpoints:
        
#         #pairs=[]
#         if(len(l)<=75):
        
#             for i in range(len(l)-1):
#                  pair=[]
#                  pair.append(l[i])
#                  for j in range(i+1,len(l)):
#                  #pairs.append([l[i],l[j]])
#                      pair.append(l[j])
#                      pair.sort()
#                      interval_bin=[]
#                      lst_cp.append(str(pair[0]) + "<=" + col_names[ctr] + "<" + str(pair[1]))
#                      for k in temp[ctr]:
#                          if(k>= pair[0] and k<= pair[1]):
#                              interval_bin.append(1)
#                          else:
#                              interval_bin.append(0)
#                      pair =[]
#                      pair.append(l[i])
#                      all_interval_bin.append(interval_bin)
#      #ctr =ctr +1
#      #print(pairs)
#      #cp_pairs.append(pairs)
#     print("CP PAIRS = ",len(lst_cp))
#     interval_df = pd.DataFrame(all_interval_bin)
#     interval_df = interval_df.transpose()
#     interval_df.columns=lst_cp
    
#     final_bin_df = pd.concat([level_df,interval_df],axis=1) #if axis != 1 then coordinate product is taken 
# #    print(final_bin_df)
#     #result_list=original_df[result_col].tolist()
# #    print(result_list)
#     final_bin_df['result']=result_list
#     return final_bin_df
    
    final_bin_df = level_df.copy()
    
    #result_list=original_df[result_col].tolist()
    
    final_bin_df['result']=result_list
    return final_bin_df

                
           
                    
        
    
        
    

#START OF PROGRAM
#READ DATA FILE
#df=pd.read_csv(r'C:\Users\user\Dropbox\lad\final lad code\checked  result\KDDTRAIN_CSV_numerical2.csv')
# df=pd.read_csv(r'F:\SNEHA PHD 15 OCT 2021\PhD work JAN 2022\UNSW B15\UNSW_NB15_training-set - Copy.csv')
df=pd.read_csv(r'UNSW_2018_IoT_Botnet_Final_10_best_Training-50k.csv') #'02-14-2018-0benign-1rest.csv')

# df_min_max_scaled = df.copy()
# df_min_max_scaled = df_min_max_scaled.drop("Label",axis=1)

# apply normalization techniques
# for column in df_min_max_scaled.columns:
#     df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())

# print(df_min_max_scaled)
# df_min_max_scaled["Label"] = df["Label"]
# df = df_min_max_scaled.copy()
# print(df)

# class_0 = df[df["Label"]==0]
# class_1 = df[df["Label"]==1]
# train_0, test_0 = train_test_split(class_0, test_size=0.3,random_state = 24, shuffle=True)
# train_1, test_1 = train_test_split(class_1, test_size=0.3,random_state = 24, shuffle=True)
# train = pd.concat([train_0,train_1])  #here train has large rows and test has small no of rows. so test is used to build lad classifier and train part is used for testing
# test = pd.concat([test_0,test_1])

# print(train)

# df= test

# y="file8\\remove duplicate and 50k rows\\02-28-2018-50k-largepart.csv"
# train.to_csv(y,index=None)
# y="file8\\remove duplicate and 50k rows\\02-28-2018-50k-trainpart.csv"
# test.to_csv(y,index=None)

head_list=[]
for col in df.columns:
    head_list.append(col)
#print(head_list)
bin_data = num(df)


#create final csv file
y= "D:\\IDEAL 2023 work 13 sept\\Iot-train-50k-bin.csv"
bin_data.to_csv(y,index=None)
