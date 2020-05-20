# -*- coding: utf-8 -*-
import tkinter as tk
import gui_fun_filemaker_v3 as fun
import auto_complete as auto

root = tk.Tk()
root.title("Get diagnosis or chart")
root.geometry("800x600")
toptext = tk.Label(root, text='抽出する条件を設定してください')
toptext.pack()
"""
variable
"""
read = tk.StringVar()
save = tk.StringVar()
ID = tk.StringVar()
age = tk.StringVar()
sex = tk.StringVar()
#disease_first = tk.StringVar()
disease_last = tk.StringVar()
part = tk.StringVar()
#privacy = tk.StringVar()

check_read = tk.BooleanVar()
check_save = tk.BooleanVar()
check_ID = tk.BooleanVar()
check_age = tk.BooleanVar()
check_sex = tk.BooleanVar()
#check_disease_first = tk.BooleanVar()
check_disease_last = tk.BooleanVar()
check_part = tk.BooleanVar()
#check_privacy = tk.BooleanVar()

check_read.set(False)
check_save.set(False)
check_ID.set(False)
check_age.set(False)
check_sex.set(False)
#check_disease_first.set(False)
check_disease_last.set(False)
check_part.set(False)
#check_privacy.set(False)

"""
text&entry
"""
text0 = tk.Label(root, text='Diagnosis search')
text0.pack()

frame_read = tk.Frame(root, pady=10)
frame_read.pack()
L_read = tk.Label(frame_read, text="csvfile_read")
L_read.grid(column=1, row=1)
E_read = tk.Entry(frame_read, bd=1)
#E_read.insert(0, "None")
E_read.insert(0, "savefile.csv")
E_read.grid(column=2, row=1)
C_read = tk.Checkbutton(frame_read, variable=check_read)
C_read.grid(column=3, row=1)
"""
frame_save = tk.Frame(root, pady=10)
frame_save.pack()
L_save = tk.Label(frame_save, text="csvfile_save")
L_save.grid(column=1, row=1)
E_save = tk.Entry(frame_save, bd=1)
#E_save.insert(0, "None")
E_save.insert(0, "outputfile.csv")
E_save.grid(column=2, row=1)
C_save = tk.Checkbutton(frame_save, variable=check_save)
C_save.grid(column=3, row=1)
"""
frame_disease_last = tk.Frame(root, pady=10)
frame_disease_last.pack()
L_disease_last = tk.Label(frame_disease_last, text="diagnosis(必須)")
L_disease_last.grid(column=1, row=1)


E_disease_last = auto.MainFrame(frame_disease_last)
#E_disease_last = tk.Entry(frame_disease_last, bd=1)

#E_disease_last.insert(0, "diagnosis")

E_disease_last.grid(column=2, row=1)
C_disease_last = tk.Checkbutton(frame_disease_last, variable=check_disease_last)
C_disease_last.grid(column=3, row=1)

frame_age = tk.Frame(root, pady=10)
frame_age.pack()
L_age = tk.Label(frame_age, text="Age")
L_age.grid(column=1, row=1)
E_age = tk.Entry(frame_age, bd=1)
E_age.insert(0, "None")
E_age.grid(column=2, row=1)
C_age = tk.Checkbutton(frame_age, variable=check_age)
C_age.grid(column=3, row=1)

frame_sex = tk.Frame(root, pady=10)
frame_sex.pack()
L_sex = tk.Label(frame_sex, text="sex(male or female)")
L_sex.grid(column=1, row=1)
E_sex = tk.Entry(frame_sex, bd=1)
E_sex.insert(0, "None")
E_sex.grid(column=2, row=1)
C_sex = tk.Checkbutton(frame_sex, variable=check_sex)
C_sex.grid(column=3, row=1)
"""
frame_disease_first = tk.Frame(root, pady=10)
frame_disease_first.pack()
L_disease_first = tk.Label(frame_disease_first, text="initial_diagnosis")
L_disease_first.grid(column=1, row=1)
E_disease_first = tk.Entry(frame_disease_first, bd=1)
E_disease_first.insert(0, "None")
E_disease_first.grid(column=2, row=1)
C_disease_first = tk.Checkbutton(frame_disease_first, variable=check_disease_first)
C_disease_first.grid(column=3, row=1)
"""

frame_part = tk.Frame(root, pady=10)
frame_part.pack()
L_part = tk.Label(frame_part, text="part")
L_part.grid(column=1, row=1)
E_part = tk.Entry(frame_part, bd=1)
E_part.insert(0, "None")
E_part.grid(column=2, row=1)
C_part = tk.Checkbutton(frame_part, variable=check_part)
C_part.grid(column=3, row=1)


"""
frame_privacy = tk.Frame(root, pady=10)
frame_privacy.pack()
L_privacy = tk.Label(frame_privacy, text="Yes or No")
L_privacy.grid(column=1, row=1)
E_privacy = tk.Entry(frame_privacy, bd=1)
E_privacy.insert(0, "No")
E_privacy.grid(column=2, row=1)
C_privacy = tk.Checkbutton(frame_privacy, variable=check_privacy)
C_privacy.grid(column=3, row=1)
"""


"""
button
"""
def diag_get():
    # Entryウィジェットのテキストを読み取るgetメソッド
    if check_age.get() and check_sex.get() and check_disease_last.get() and check_part.get() and (not check_ID.get()):
        text_read = E_read.get()
        text_age = E_age.get()
        text_sex = E_sex.get()
        text_disease_last = E_disease_last.getdrop()
        text_part = E_part.get()

        fun.gui_diagnosis(text_read, text_age, text_sex, text_disease_last, text_part)

        #print(test_read, test_save, text_ID, text_age, text_sex, text_disease_first, text_disease_last, text_part, text_privacy)
        print("OK")
    else:
        print("check age and sex and diagnosis and part! or uncheck ID")

button_diag = tk.Button(root,text="GET",command=diag_get)
button_diag.pack()

text1 = tk.Label(root, text='Chart search')
text1.pack()

frame_ID = tk.Frame(root, pady=10)
frame_ID.pack()
L_ID = tk.Label(frame_ID, text="ID")
L_ID.grid(column=1, row=1)
E_ID = tk.Entry(frame_ID, bd=1)
E_ID.insert(0, "None")
E_ID.grid(column=2, row=1)
C_ID = tk.Checkbutton(frame_ID, variable=check_ID)
C_ID.grid(column=3, row=1)

def chart_get():
    # Entryウィジェットのテキストを読み取るgetメソッド
    if check_ID.get() and not (check_age.get() or check_sex.get() or check_disease_last.get() or check_part.get()):
        text_read = E_read.get()
        text_ID = E_ID.get()

        fun.gui_chart(text_read, text_ID)

        #print(test_read, test_save, text_ID, text_age, text_sex, text_disease_first, text_disease_last, text_part, text_privacy)
        print("OK")
    else:
        print("check! ID! or uncheck! others")

button_chart = tk.Button(root,text="GET",command=chart_get)
button_chart.pack()

root.mainloop()
