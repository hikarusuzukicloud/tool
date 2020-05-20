import copy
import os
from tkinter import *
from datetime import datetime

from PIL import Image, ImageTk

imagedir = "./data/"
savedir = "./save/"
readtxtfilename = "folder.txt"
txtdefault = "drug_eruption"
CANPUS_SIZE = 700

class MainWindow():
    def __init__(self, main):
        # 画像を表示するキャンバスを作る
        self.canvas = Canvas(main, width=CANPUS_SIZE, height=CANPUS_SIZE)
        self.canvas.pack()

        #フォルダリスト読み込み
        with open(readtxtfilename, "r") as fr:
            self.folders = fr.readlines()

        self.defaultfolders = copy.deepcopy(self.folders)
        self.savefolder = []
        for i in range(len(self.folders)):
            os.makedirs(savedir + "crop_" + self.folders[i].strip(), exist_ok=True)
            self.savefolder.append(savedir + "crop_" + self.folders[i].strip())
        for i in range(len(self.folders)):
            self.folders[i] = imagedir + self.folders[i].strip()

        self.folder_num = 0
        self.current_folder = self.folders[self.folder_num]
        self.current_savefolder = self.savefolder[self.folder_num]

        self.my_images = []
        self.file_num = 0
        self.my_images_name = []
        self.my_images_default_name = []
        self.my_images = []
        self.my_image_number = 0
        self.save_file_num = 0

        self.get_folder()

        # 最初の画像をセット
        #self.image_on_canvas = self.canvas.create_image(
        #    0, 0, anchor=NW, image=self.my_images[self.my_image_number])
        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor=NW)
        self.canvas.itemconfig(self.image_on_canvas,
                               image=self.my_images[self.my_image_number])

        # メッセージを表示するEntryを作る
        # 現在の画像番号を表示するEntry
        self.message_num = Entry(width=80)
        self.correntfilename = self.my_images_name[self.my_image_number]
        self.message_num.insert(END, self.correntfilename)
        self.message_num.pack()

        # 次の保存番号を表示するEntry
        self.message = Entry(width=80)
        self.savefilename = self.current_savefolder +  "/crop_" + str(self.save_file_num) + "_" + self.my_images_default_name[self.my_image_number]
        self.message.insert(END, self.savefilename)
        self.message.pack()

        # 画像切り出し用のラインをキャンバスに描画
        self.tag_line_list = ["left_line", "right_line", "top_line", "bottom_line"]
        self.color_line_list = ["green", "red", "green", "red"]

        self.canvas.create_line(0, 0, 0, self.my_images[self.my_image_number].height(),
                                tag=self.tag_line_list[0], fill=self.color_line_list[0])
        self.canvas.create_line(self.my_images[self.my_image_number].width(), 0,
                                self.my_images[self.my_image_number].width(), self.my_images[self.my_image_number].height(),
                                tag=self.tag_line_list[1], fill=self.color_line_list[1])
        self.canvas.create_line(0, 0, self.my_images[self.my_image_number].width(), 0,
                                tag=self.tag_line_list[2], fill=self.color_line_list[2])
        self.canvas.create_line(0, self.my_images[self.my_image_number].height(),
                                self.my_images[self.my_image_number].width(), self.my_images[self.my_image_number].height(),
                                tag=self.tag_line_list[3], fill=self.color_line_list[3])

        self.point = [0, self.my_images[self.my_image_number].width(), 0, self.my_images[self.my_image_number].height()]

        #モードの初期設定
        self.mode = 0

        #mode切り替えイベント
        #self.canvas.bind("<Key>", self.mode_change)
        self.canvas.bind("a", self.mode_change)
        self.canvas.bind("d", self.mode_change)
        self.canvas.bind("w", self.mode_change)
        self.canvas.bind("s", self.mode_change)
        self.canvas.focus_set()
        #self.pack()

        #クリックされた時のカーソル移動
        #canvas内がクリックされた時のみ
        self.canvas.bind("<Button-1>", self.line_set)

        #actions
        self.canvas.bind("b", self.back_action)
        self.canvas.bind("f", self.next_action)
        self.canvas.bind("<space>", self.save_action)
        self.canvas.bind("g", self.backsave_action)
        self.canvas.bind("r", self.change_folder)
        self.canvas.bind("t", self.change_folder)
        self.canvas.bind("y", self.txtsave)


    def get_folder(self):
        pattern = re.compile('.*[.](JPG|jpg|jpeg|png)$')
        self.my_images_name = [self.current_folder + "/" + image for image in os.listdir(self.current_folder) if re.match(pattern, image)]
        self.my_images_default_name = [image for image in os.listdir(self.current_folder) if re.match(pattern, image)]
        self.my_images_name.sort()
        self.my_images_default_name.sort()
        self.my_images = []
        for i in self.my_images_default_name:
            readname = os.path.join(self.current_folder, i)
            image = Image.open(readname)
            if image.width > image.height:
                image_resize = image.resize((700, int(image.height * CANPUS_SIZE / image.width)))
            else:
                image_resize = image.resize((int(image.width * CANPUS_SIZE / image.height), 700))
            self.my_images.append(ImageTk.PhotoImage(image_resize))

    def change_folder(self, event):
        if event.char == "r":
            self.folder_num += 1
            if self.folder_num == len(self.folders):
                self.folder_num = 0

        if event.char == "t":
            if self.folder_num == 0:
                self.folder_num = len(self.folders) - 1
            else:
                # 一つ戻る
                self.folder_num -= 1

        self.current_folder = self.folders[self.folder_num]
        self.current_savefolder = self.savefolder[self.folder_num]
        self.get_folder()

        #reset
        self.file_num = 0
        self.my_image_number = 0
        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor=NW, image=self.my_images[self.my_image_number])
        self.mode = 0
        self.line_reset()

        # Entryの中身を更新
        self.message_num.delete(0, END)
        self.correntfilename = self.my_images_name[self.my_image_number]
        self.message_num.insert(END, self.correntfilename)

        self.message.delete(0, END)
        self.savefilename = self.current_savefolder +  "/crop_" + str(self.save_file_num) + "_" + self.my_images_default_name[self.my_image_number]
        self.message.insert(END, self.savefilename)

    def mode_change(self, event):
        if event.char == "a":
            self.mode = 0
        if event.char == "d":
            self.mode = 1
        if event.char == "w":
            self.mode = 2
        if event.char == "s":
            self.mode = 3

    def line_set(self, event):
        self.canvas.delete(self.tag_line_list[self.mode])
        if self.mode == 0 or self.mode == 1:
            self.point[self.mode] = event.x
            self.canvas.create_line(event.x, 0, event.x, self.my_images[self.my_image_number].height(),
                                    tag=self.tag_line_list[self.mode], fill=self.color_line_list[self.mode])
        else:
            self.point[self.mode] = event.y
            self.canvas.create_line(0, event.y, self.my_images[self.my_image_number].width(), event.y,
                                    tag=self.tag_line_list[self.mode], fill=self.color_line_list[self.mode])

    def line_reset(self):
        for i in range(4):
            self.canvas.delete(self.tag_line_list[i])
        self.canvas.create_line(0, 0, 0, self.my_images[self.my_image_number].height(),
                                tag=self.tag_line_list[0], fill=self.color_line_list[0])
        self.canvas.create_line(self.my_images[self.my_image_number].width(), 0,
                                self.my_images[self.my_image_number].width(), self.my_images[self.my_image_number].height(),
                                tag=self.tag_line_list[1], fill=self.color_line_list[1])
        self.canvas.create_line(0, 0, self.my_images[self.my_image_number].width(), 0,
                                tag=self.tag_line_list[2], fill=self.color_line_list[2])
        self.canvas.create_line(0, self.my_images[self.my_image_number].height(),
                                self.my_images[self.my_image_number].width(), self.my_images[self.my_image_number].height(),
                                tag=self.tag_line_list[3], fill=self.color_line_list[3])

        self.point = [0, self.my_images[self.my_image_number].width(), 0, self.my_images[self.my_image_number].height()]

        self.mode = 0

    def back_action(self, event):
        # 最後の画像に戻る
        if self.my_image_number == 0:
            self.my_image_number = len(self.my_images) - 1
        else:
            # 一つ戻る
            self.my_image_number -= 1

        # 表示画像を更新
        self.canvas.itemconfig(self.image_on_canvas,
                               image=self.my_images[self.my_image_number])
        self.line_reset()

        # Entryの中身を更新
        self.message_num.delete(0, END)
        self.correntfilename = self.my_images_name[self.my_image_number]
        self.message_num.insert(END, self.correntfilename)

        self.message.delete(0, END)
        self.savefilename = self.current_savefolder +  "/crop_" + str(self.save_file_num) + "_" + self.my_images_default_name[self.my_image_number]
        self.message.insert(END, self.savefilename)

    def next_action(self, event):
        # 一つ進む
        self.my_image_number += 1

        # 最初の画像に戻る
        if self.my_image_number == len(self.my_images):
            self.my_image_number = 0

        # 表示画像を更新 "
        self.canvas.itemconfig(self.image_on_canvas,
                               image=self.my_images[self.my_image_number])
        self.line_reset()

        # Entryの中身を更新
        self.message_num.delete(0, END)
        self.correntfilename = self.my_images_name[self.my_image_number]
        self.message_num.insert(END, self.correntfilename)

        self.message.delete(0, END)
        self.savefilename = self.current_savefolder +  "/crop_" + str(self.save_file_num) + "_" + self.my_images_default_name[self.my_image_number]
        self.message.insert(END, self.savefilename)

    def save_action(self, event):
        # 表示画像を取り込み
        self.temp_image = Image.open(self.my_images_name[self.my_image_number])
        # 選択位置で切り出し
        if self.temp_image.width > self.temp_image.height:
            scale = self.temp_image.width / CANPUS_SIZE
        else:
            scale = self.temp_image.height / CANPUS_SIZE
        self.cropped_image = self.temp_image.crop(
            (int(scale * self.point[0]), int(scale * self.point[2]), int(scale * self.point[1]), int(scale * self.point[3])))
        self.cropped_image.save(self.current_savefolder +  "/crop_" + str(self.save_file_num) + "_" + self.my_images_default_name[self.my_image_number])

        self.save_file_num += 1

        # Entryの中身を更新
        self.message.delete(0, END)
        self.savefilename = self.current_savefolder +  "/crop_" + str(self.save_file_num) + "_" + self.my_images_default_name[self.my_image_number]
        self.message.insert(END, self.savefilename)

    def backsave_action(self, event):
        self.save_file_num -= 1

        if self.save_file_num == -1:
            self.save_file_num = 0

        # Entryの中身を更新
        self.message.delete(0, END)
        self.savefilename = self.current_savefolder +  "/crop_" + str(self.save_file_num) + "_" + self.my_images_default_name[self.my_image_number]
        self.message.insert(END, self.savefilename)

    def txtsave(self, event):
        today = datetime.today()
        today_str = today.strftime("%m") + "_" +today.strftime("%m") + "_" +today.strftime("%H")
        txtsavename = "list_" + txtdefault + "_" + today_str + ".txt"
        with open(txtsavename, "w") as fw:
            for i in range(len(self.folders) - self.folder_num):
                #fw.write(self.defaultfolders[self.folder_num + i] + "\n")
                fw.write(self.defaultfolders[self.folder_num + i])


if __name__ == '__main__':
    root = Tk()
    root.title("Crop Tool")
    root.geometry("{}x{}".format(CANPUS_SIZE+5, CANPUS_SIZE + 60))
    MainWindow(root)
    root.mainloop()
