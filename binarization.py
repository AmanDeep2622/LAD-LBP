
import pandas as pd
import gc
# from sklearn.model_selection import train_test_split

# FUNCTION NUM
def num(df):
    result_col = "class" #input("enter name of result column")
    all_cutpoints=[]
    original_df=df.copy()
    # result_list = original_df[result_col]
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
    

    
    final_bin_df = level_df.copy()
    
    #result_list=original_df[result_col].tolist()
    
    final_bin_df['result']=result_list
    return final_bin_df


df = pd.read_csv(r'KDDTRAIN_CSV_numerical-25k.csv',nrows=25000)

head_list=[]
for col in df.columns:
    head_list.append(col)
#print(head_list)
bin_data = num(df)


#create final csv file
y= "HG/bin1.csv"
bin_data.to_csv(y,index=None)
