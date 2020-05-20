# -*- coding: utf-8 -*-
import re
import os
import csv
import pickle

import numpy as np
import pandas as pd

def input_diagkind():
    print("ini->0, fi->1")
    while(True):
        kind_no = int(input())
        if kind_no == 0:
            diag_kind = 'ini'
            break
        elif kind_no == 1:
            diag_kind = 'fi'
            break
    return diag_kind

def input_methodnum(METHOD_NUM, method_list):
    for i in range(len(method_list)):
        print(method_list[i] + "->" + str(i))
    method = 10
    while(method < 0 or method > METHOD_NUM):
        method = int(input())
    return method

def count_unique(data, diags, diag_kind, method_str):
    diag_count = []
    for d, index in diags.items():
        count = 0
        pat_list = []#この場所に置くことによって病気ごとにリセット
        if not index == []:
            for i in index:
                df = data[i:i+1]
                pat_id =  df.iat[0, 3] + "_" + str(int(df.iat[0, 1]))
                if not pat_id in pat_list:
                    pat_list.append(pat_id)
                    count += 1
        diag_count.append([d, count])
    return diag_count

def count_sex(data, diags, diag_kind, method_str):
    diag_count_sex = []
    for d, index in diags.items():
        count_male = 0
        count_female = 0
        count_unknown = 0
        pat_list = []
        if not index == []:
            for i in index:
                df = data[i:i+1]
                pat_id =  df.iat[0, 3] + "_" + str(int(df.iat[0, 1]))
                if not pat_id in pat_list:
                    sex = df.iat[0, 5]
                    if sex == "male":
                        count_male += 1
                    elif sex == "female":
                        count_female += 1
                    else:
                        count_unknown += 1
                    pat_list.append(pat_id)
        if (count_male + count_female) != 0:
            male_rate = count_male / (count_male + count_female)
            female_rate = count_female / (count_male + count_female)
        else:
            male_rate = 0
            female_rate = 0
        diag_count_sex.append([d, count_male, count_female, male_rate, female_rate, count_unknown])
    return diag_count_sex

def count_university(data, diags, diag_kind, method_str):
    uni_list = ["HM", "KC", "KM", "KO", "KS", "KT", "NG", "RK", "SS", "TB", "TK", "YN"]
    diag_count_uni = []
    for d, index in diags.items():
        pat_list = []
        uni_count = [0 for i in range(len(uni_list))]
        if not index == []:
            for i in index:
                df = data[i:i+1]
                uni = df.iat[0, 3]
                pat_id =  uni + "_" + str(int(df.iat[0, 1]))
                if not pat_id in pat_list:
                    for (j, s) in enumerate(uni_list):
                        if s in uni:
                            uni_count[j] += 1
                            break
                    pat_list.append(pat_id)
        diag_count_uni.append([d] + uni_count)
    return diag_count_uni

def count_age(data, diags, diag_kind, method_str):
    #age = 10, 20, 30, 40, 50, 60, 70, 80
    diag_count_age = []
    for d, index in diags.items():
        pat_list = []
        age_count = [0 for i in range(101)]
        if not index == []:
            for i in index:
                df = data[i:i+1]
                age = df.iat[0, 4]
                if type(age) is str:
                    if age.isdecimal():
                        age = int(age)
                    elif (age.replace(".", "")).isdecimal():
                        age = int(float(age))
                    elif (age.replace("　", "")).isdecimal():
                        age = int(float(age))
                    elif "m" in age or "M" in age or "月" in age or "日" in age or "Ｍ" in age or "ｍ" in age:
                        age = 0
                    else:
                        continue
                if not (type(age) is np.int64 or type(age) is int or type(age) is float):
                    continue
                pat_id =  df.iat[0, 3] + "_" + str(int(df.iat[0, 1]))
                if not pat_id in pat_list:
                    if age >= 0 and age < 100:
                        age_count[age] += 1
                    elif age >= 100 and age < 130:
                        age_count[100] += 1
                    pat_list.append(pat_id)
        diag_count_age.append([d] + age_count)
    return diag_count_age

def count_part(data, diags, diag_kind, method_str):
    part_list = ["Face", "Scalp", "Trunk", "Leg", "UpperArm", "Whole body", "Unknown"]
    diag_count_part = []
    for d, index in diags.items():
        pat_list = []
        part_count = [0 for i in range(len(part_list))]
        if not index == []:
            for i in index:
                df = data[i:i+1]
                part = df.iat[0, 9]
                pat_id = df.iat[0, 3] + "_" + str(int(df.iat[0, 1]))
                if not pat_id in pat_list:
                    for (j, s) in enumerate(part_list):
                        #breakしないことでpartを/で分解する必要がない
                        if s in part:
                            part_count[j] += 1
                    pat_list.append(pat_id)
        diag_count_part.append([d] + part_count)
    return diag_count_part

def method_count(method, data, diags, diag_kind, method_str):
    if method == 1:
        countlist = count_unique(data, diags, diag_kind, method_str)
    elif method == 2:
        countlist = count_sex(data, diags, diag_kind, method_str)
    elif method == 3:
        countlist = count_university(data, diags, diag_kind, method_str)
    elif method == 4:
        countlist = count_age(data, diags, diag_kind, method_str)
    elif method == 5:
        countlist = count_part(data, diags, diag_kind, method_str)
    else:
        return
    savefilename = "countlist_st_diag_" + method_str + "_" + diag_kind + ".pickle" 
    with open(savefilename, 'wb') as fsave:
        pickle.dump(countlist, fsave, 4)

def main():
    METHOD_NUM = 5
    method_list = ["all", "num", "sex", "uni", "age", "part"]
    diag_kind = input_diagkind()
    method = input_methodnum(METHOD_NUM, method_list)
    csvfile = "staticsdata.csv"
    readfilename = "each_diag_index_" + diag_kind + ".pickle"
    data = pd.read_csv(csvfile)
    with open(readfilename, 'rb') as fdic:
        diags = pickle.load(fdic)
        if method != 0:
            method_count(method, data, diags, diag_kind, method_list[method])
        elif method == 0:
            for i in range(1, METHOD_NUM + 1):
                method_count(i, data, diags, diag_kind, method_list[i])

if __name__=='__main__':
    main()
