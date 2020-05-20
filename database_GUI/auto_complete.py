import tkinter as tk
import tkinter.ttk as ttk
import csv
 
 
with open("d_list_save.csv", "r") as f:
    data = csv.reader(f)
    for i in data:
        BUILTIN_KEYWORD = i

class MainFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        """ウィジェットの作成、配置"""
        #self.text = tk.Text(self, bd=1)
        #self.text.grid(column=2, row=1)

        self.text = tk.Text(self, height=9)
        self.text.grid(column=2, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Tab押下時(インデント、又はコード補完)
        self.text.bind('<Tab>', self.tab)

        self.text.columnconfigure(0, weight=1)
        self.text.rowconfigure(0, weight=1)

    def tab(self, event=None):
        """タブ押下時の処理"""
        # 文字を選択しておらず...
        sel_range = self.text.tag_ranges('sel')
        if not sel_range:
            # インサートカーソルの前の文字がタブ、スペース、空文字、改行じゃない
            before_insert_text = self.text.get('insert-1c', 'insert')
            if before_insert_text not in (' ', '\t', '\n', ''):
                return self.auto_complete()

    def auto_complete(self):
        """補完リストの作成"""
        auto_complete_list = tk.Listbox(self.text)
 
        # エンターでそのキーワードを選択
        auto_complete_list.bind('<Return>', self.selection)
 
        # エスケープ、タブ、他の場所をクリックで補完リスト削除
        auto_complete_list.bind('<Escape>', self.remove_list)
        auto_complete_list.bind('<Tab>', self.remove_list)
        auto_complete_list.bind('<FocusOut>', self.remove_list)
 
        # (x,y,width,height,baseline)
        x, y, _, height, _ = self.text.dlineinfo(
            'insert')
        # 現在のカーソル位置のすぐ下に補完リストを貼る
        auto_complete_list.place(x=x, y=y+height)
 
        # 補完リストの候補を作成
        for word in self.get_keywords():
            auto_complete_list.insert(tk.END, word)
 
        # 補完リストをフォーカスし、0番目を選択している状態に
        auto_complete_list.focus_set()
        auto_complete_list.selection_set(0)
        self.auto_complete_list = auto_complete_list  # self.でアクセスできるように
        return 'break'

    def get_keywords(self):
        """コード補完リストの候補キーワードを作成する."""
        # 現在入力中の単語を取得
        text, _, _ = self.get_current_insert_word()
        # 組み込みの関数、例外クラス
        #BUILTIN_KEYWORD = ['Python', 'Ruby', 'PHP', 'Perl', "Pycharm"]
        return [x for x in BUILTIN_KEYWORD if x.startswith(text) or x.startswith(text.title())]

    def remove_list(self, event=None):
        """コード補完リストの削除処理."""
        self.auto_complete_list.destroy()
        self.text.focus()  # テキストウィジェットにフォーカスを戻す

    def selection(self, event=None):
        """コード補完リストでの選択後の処理."""
        # リストの選択位置を取得
        select_index = self.auto_complete_list.curselection()
        if select_index:
            # リストの表示名を取得
            value = self.auto_complete_list.get(select_index)
 
            # 現在入力中の単語位置の取得
            _, start, end = self.get_current_insert_word()
            self.text.delete(start, end)
            self.text.insert('insert', value)
            self.remove_list()

    def get_current_insert_word(self):
        """現在入力中の単語と位置を取得する."""
        text = ''
        start_i = 1
        end_i = 0
        
        while True:
            start = 'insert-{0}c'.format(start_i)
            end = 'insert-{0}c'.format(end_i)
            text = self.text.get(start, end)
 
            # 1文字ずつ見て、スペース、改行、タブ、空文字にぶつかったら終わり
            if text in (' ', '\t', '\n', ''):
                text = self.text.get(end, 'insert')
                return text, end, 'insert'
 
            start_i += 1
            end_i += 1

    def getdrop(self):
        return self.text.get('1.0', 'insert')


if __name__ == '__main__':
    root = tk.Tk()
    app = MainFrame(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()
