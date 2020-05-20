# -*- coding: utf-8 -*-
import csv
import os
from operator import itemgetter
import math

import numpy as np
import pandas as pd
import scipy as sp
import scipy.stats
import matplotlib.pyplot as plt
from lifelines.statistics import logrank_test
from lifelines import KaplanMeierFitter, CoxPHFitter

def make_graph(male, female, d, savedir, p):
    if "(" in d:
        diag_sp = d.split("(")
        d = diag_sp[0]

    plt.figure(figsize=(12,6))
    #plt.grid(linestyle="--")
    plt.title("logrank, p = " + '{:.3e}'.format(p) + "\n" + d)
    plt.xlabel("age")
    plt.ylabel("pat_num")
    plt.plot(male, label="male")
    plt.plot(female, label="female")
    plt.legend()

    plt.savefig(savedir + "/plot_logrank_" + d + ".png")
    plt.close()

def make_kmf_plt(d_male, d_female, d, savedir, title):
    kmf = KaplanMeierFitter()
    kmf.fit(d_male, timeline=np.linspace(0,100,100), label="male")
    #kmf.fit(d_male, label="male")
    ax = kmf.plot()
    kmf.fit(d_female, timeline=np.linspace(0,100,100), label="female")
    #kmf.fit(d_female, label="female")
    ax = kmf.plot(ax=ax)
    if "(" in d:
        diag_sp = d.split("(")
        d = diag_sp[0]
    plt.title(title + d)
    plt.xlabel("age")
    plt.ylabel("survival")
    #plt.show()
    plt.savefig(savedir + "/plot_survival_" + d + ".png")
    plt.close()

def make_data(data):
    d = []
    for age, n in enumerate(data):
        d += [age] * n
    return d

def cox(d_male, d_female):
    df_male = pd.DataFrame({
        "time":d_male,
        "event":1,
        "sex": 0
        })
    df_female = pd.DataFrame({
        "time":d_female,
        "event":1,
        "sex": 1
        })
    df = pd.concat([df_male, df_female])
    
    print(len(d_male), len(d_female))
    cph = CoxPHFitter()
    cph.fit(df, duration_col="time", event_col="event")
    cph.print_summary()
    #print(cph.hazards_)


def main():
    savedir = "logrank"
    os.makedirs(savedir, exist_ok=True)
    file_male = "count_age_each_sex_male.csv"
    file_female = "count_age_each_sex_female.csv"
    data_male = (pd.read_csv(file_male)).values.tolist()
    data_female = (pd.read_csv(file_female)).values.tolist()
    count = 0
    count_u = 0
    result = []

    for i in range(len(data_male)):
        if data_male[i][1] < 50:
            break
        d_male = data_male[i][2::]
        d_male_list = make_data(d_male)
        d_female = data_female[i][2::]
        d_female_list = make_data(d_female)
        diag = data_male[i][0]

        
        #print(len(d_male_list))
        #print(len(d_female_list))
        #if len(d_male_list) < 20 or len(d_female_list) < 20:
        #    continue
        count += 1
        results = logrank_test(d_male_list, d_female_list)
        #results.print_summary()
        title = "logrank, p = " + '{:.3e}'.format(results.p_value) + "m" + str(len(d_male_list)) + "_f" + str(len(d_female_list)) + "\n"
        if results.p_value < 0.05:
            count_u += 1
            #print(diag)
            #print(results.p_value)
            #cox(d_male_list, d_female_list)
            #make_graph(d_male, d_female, diag, savedir, results.p_value)
            make_kmf_plt(d_male_list, d_female_list, diag, savedir, title)

        """
        else:
            make_graph(d_male, d_female, diag, "logrank_false", title)
            make_kmf_plt(d_male_list, d_female_list, diag, "logrank_false", title)
        """
        #result.append(results.p_value)
            
    """
    result.sort()
    result = [math.log10(x) for x in result]
    plt.plot(result)
    plt.show()
    """
    print("test")
    print(count)
    print("under 0.05")
    print(count_u)


if __name__=='__main__':
    main()
