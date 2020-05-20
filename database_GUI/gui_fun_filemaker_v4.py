# -*- coding: utf-8 -*-
import re
import os
import csv
import shutil
from distutils.util import strtobool

import pandas as pd

def cut_database(df, aim_age, aim_sex, aim_fidiag, aim_part, aim_count, aim_dermoscopy, aim_pathology, aim_photo, aim_race):
    aim_fidiag = aim_fidiag.split(" ")[0]
    aim_age = str(aim_age).split("-")
    df = df[df["fidiag"].str.contains(aim_fidiag)]
    if aim_sex != "None":
        df = df[df["sex"] == aim_sex]
    if aim_age != ["None"]:
        if len(aim_age) == 1:
            df = df[df["age"] == int(aim_age[0])] 
        elif len(aim_age) == 2:
            df = df[df["age"] >= int(aim_age[0])]
            df = df[df["age"] <= int(aim_age[1])]
    if aim_part != "None":
        df = df[df["part"].str.contains(aim_part)]
    if aim_dermoscopy != "None":
        df = df[df["dermos_bool"] == strtobool(aim_dermoscopy)]
    if aim_pathology != "None":
        df = df[df["patho_bool"] == strtobool(aim_pathology)]
    if aim_photo != "None":
        df = df[df["photo"].str.contains(aim_photo)]
    if aim_race != "None":
        df = df[df["race"] == aim_race]
    return df

def copyimg_count(df, aim_fidiag, aim_count, savecsvname, imgdir):
    count = 0
    aim_count = int(aim_count)
    length = df.shape[0]
    pad_id_list = []
    df = df.sample(frac=1)
    index_list = list(df.index)
    for index, item in df.iterrows():
        fidiag_list = item["fidiag"].split("/")
        id_str = str(item["ID"])
        os.makedirs(aim_fidiag + "/" + id_str, exist_ok=True)
        if aim_fidiag in fidiag_list:
            pad_id = str(item["uni_ID"]) + "_" + str(item["ID"])
            if pad_id not in pad_id_list:
                print(pad_id)
                pad_id_list.append(pad_id)
                imgpath = imgdir + id_str + "/" + item["imagefilename"]
                savepath = "./" + aim_fidiag + "/" + id_str + "/" + item["imagefilename"]
                shutil.copyfile(imgpath, savepath)
                index_list.remove(index)
                count += 1
        else:
            df.drop(index=index, inplace=True)
        if count == aim_count:
            break
    if index_list:
        df.drop(index=index_list, inplace=True)
    print(df)
    df.to_csv(savecsvname, index=False)

def copyimg(df, aim_fidiag, savecsvname, imgdir):
    for index, item in df.iterrows():
        fidiag_list = item["fidiag"].split("/")
        id_str = str(item["ID"])
        os.makedirs(aim_fidiag + "/" + id_str, exist_ok=True)
        if aim_fidiag in fidiag_list:
            imgpath = imgdir + id_str + "/" + item["imagefilename"]
            savepath = "./" + aim_fidiag + "/" + id_str + "/" + item["imagefilename"]
            shutil.copyfile(imgpath, savepath)
        else:
            df.drop(index, inplace=True)
    print(df)
    df.to_csv(savecsvname, index=False)

# diagnosis, Age, sex, part, dermoscopy, count, race, date_of_photo, pathology


def gui_diagnosis(readpath, savepath, **request_list):
    head = ("ID", "photo", "uni_ID", "date_of_birth", "age", "sex", "race", 
            "photo_bool", "inidiag_bool", "fidiag_bool",
            "inidiag", "fidiag", "part", "dermos_bool", "imagefilename")
    imgdir = "./tukuba/"
    print(readpath)
    df = pd.read_csv(readpath, names=head)
    #df = pd.read_csv(readpath)
    print(df)

    df = cut_database(df, **request_list)
    if df.empty:
        print("not found")
    else:
        aim_fidiag = request_list["aim_fidiag"]
        os.makedirs(aim_fidiag, exist_ok=True)
        if request_list["aim_count"] != "None":
            copyimg_count(df, aim_fidiag, request_list["aim_count"], savepath, imgdir)
        else:
            copyimg(df, aim_fidiag, savepath, imgdir)

def main():
    #gui_chart("savefile.csv", "th3749")
    #gui_diagnosis("alldata_test.csv", "output.csv",
    gui_diagnosis("tukuba.csv", "output.csv",
                  aim_age="None", aim_sex="None", aim_fidiag="Abscesses ", aim_part="None",
                  aim_count="None", aim_dermoscopy="None", aim_pathology="None",
                  aim_photo="None", aim_race="None")
    #gui_diagnosis("alldata_test.csv", "None", "None", "Acne fulminans (Acne fulminans_Acne maligna_Sine fulminans)", "None")
    print("OK")

if __name__=='__main__':
    main()
