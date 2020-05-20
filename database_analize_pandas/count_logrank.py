# -*- coding: utf-8 -*-
import re
import os
import csv
import pickle
from operator import itemgetter

import numpy as np
import pandas as pd

def count_age(data, diags):
    diag_count_age_male = []
    diag_count_age_female = []
    for d, index in diags.items():
        pat_list = []
        pat_count = 0
        age_count_male = [0 for i in range(101)]
        age_count_female = [0 for i in range(101)]
        if index == []:
            continue
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
            sex = df.iat[0, 5]
            pat_id =  df.iat[0, 3] + "_" + str(int(df.iat[0, 1]))
            if sex == "male":
                if not pat_id in pat_list:
                    if age >= 0 and age < 100:
                        age_count_male[age] += 1
                    elif age >= 100 and age < 130:
                        age_count_male[100] += 1
                    pat_count += 1
                    pat_list.append(pat_id)
            elif sex == "female":
                if not pat_id in pat_list:
                    if age >= 0 and age < 100:
                        age_count_female[age] += 1
                    elif age >= 100 and age < 130:
                        age_count_female[100] += 1
                    pat_count += 1
                    pat_list.append(pat_id)
        diag_count_age_male.append([d, pat_count] + age_count_male)
        diag_count_age_female.append([d, pat_count] + age_count_female)

    diag_count_age_male.sort(key=itemgetter(1), reverse=True)
    diag_count_age_female.sort(key=itemgetter(1), reverse=True)
    head = ["diagnosis", "pat_count_all"] + [i for i in range(100)] + ["100over"]
    savefilename = "count_age_each_sex_male.csv"
    with open(savefilename, "w") as fm:
        writer = csv.writer(fm, lineterminator='\n')
        writer.writerows([head] + diag_count_age_male) 
    savefilename = "count_age_each_sex_female.csv"
    with open(savefilename, "w") as ff:
        writer = csv.writer(ff, lineterminator='\n')
        writer.writerows([head] + diag_count_age_female) 

def main():
    csvfile = "allunidata/staticsdata.csv"
    readfilename = "allunidata/each_diag_index_fi.pickle"
    data = pd.read_csv(csvfile)
    with open(readfilename, 'rb') as fdic:
        diags = pickle.load(fdic)
        count_age(data, diags)

if __name__=='__main__':
    main()
