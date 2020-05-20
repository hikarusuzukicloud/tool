# -*- coding: utf-8 -*-
import re
import os
import csv
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
年齢の線形グラフ
部位の円グラフ
x:age
y:pat_num
"""
def main():
    savedir = "statics_age/age_plot"
    os.makedirs(savedir, exist_ok=True)
    csvfile = "statics_age/diag_age_rate_rank.csv"
    data = pd.read_csv(csvfile)
    head = list(data.columns)
    data = data.values.tolist()

    x = head[2:13]

    for d in data:
        if float(d[1]) > 0.35:
            y = d[2:13]
            diag = d[0]

            if "(" in diag:
                diag_sp = diag.split("(")
                diag = diag_sp[0]

            plt.figure(figsize=(12,6))
            plt.grid(linestyle="--")
            plt.title("AGE RATE\n" + diag)
            plt.xlabel("age")
            plt.ylabel("rate")
            plt.plot(x, y)

            plt.savefig(savedir + "/" + "plot_age_" + diag + ".png")



if __name__=='__main__':
    main()
