import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import ImageGrab, Image, ImageTk
import os
import random
import pyautogui as py
py.FAILSAFE = False
full_path=None
HEX = None
label = None
HEX_C = "#ffffff"
xw = yw = xs = ys = xc = yc = oval = oval2 = photo = r = o = l = open_ = None, None, None, None, None, None, None, None, None, None, None, None, None
state = 0
bg_state = 0
c_state = 0
s_state = 0
r_state = 0
state = 0
step = 1
b_all=[]
o_all=[]
_all=[]
clears=[]
open_btn = None
w_info = tk.Tk()
w_info.title("Справка (f5-я понял)")
def START(event=None):
    global HEX, xw, yw, xc, yc, xs, ys, state, oval, oval2, _all, bg_state, b_all, o_all, c_count, clears, s_state, s, open_btn, label, state, r_state, step, undo_stack
    try:
        w_info.unbind("<F5>")
        w_info.destroy()
    except:
        pass
    window = tk.Tk()
    window.state("zoomed")
    window.title("Рисовашка")
    _all.append(window)
    canvas = tk.Canvas(window, height=525, width=1000, bg="white")
    canvas.pack(pady=0)
    canvas.config(cursor="tcross")
    def bg_c(event=None):
        global bg_state, b_all
        if bg_state == 0:
            for _ in range(0, len(b_all)):
                b_all[_].config(bg="black", fg="white")
            for _ in range(0, len(o_all)):
                o_all[_].config(highlightbackground="black")
            for _ in range(0, len(_all)):
                _all[_].config(bg="black")
            bg_btn.config(text="Светлая тема")
            long.config(bg="white")
            bg_state = 1
        elif bg_state == 1:
            for _ in range(0, len(b_all)):
                b_all[_].config(bg="white", fg="black")
            for _ in range(0, len(_all)):
                _all[_].config(bg="white")
            for _ in range(0, len(o_all)):
                o_all[_].config(highlightbackground="white")
            bg_btn.config(text="Сepaя тема")
            long.config(bg="white")
            bg_state = 2
        elif bg_state == 2:
            for _ in range(0, len(b_all)):
                b_all[_].config(bg="#303030", fg="white")
            for _ in range(0, len(_all)):
                _all[_].config(bg="#303030")
            for _ in range(0, len(o_all)):
                o_all[_].config(highlightbackground="#303030")
            bg_btn.config(text="Тёмная тема")
            long.config(bg="#303030")
            bg_state = 0            
    bg_btn=tk.Button(window, text="Тёмная тема")
    bg_btn.place(x=1200, y=100)
    bg_btn.config(command=bg_c)
    b_all.append(bg_btn)
    long = tk.Canvas(window, height=105, width= 105)
    long.place(x=900, y=535)
    o_all.append(long)
    _all.append(long)
    def color_cnv(event=None):
        global HEX_C, state, clears
        state = 0
        color = colorchooser.askcolor(title="Выберите цвет фона")
        if color[1]:
            HEX_C = color[1]
            canvas.config(bg=HEX_C)
            for _ in range(0, len(clears)):
                canvas.itemconfig(clears[_],fill=HEX_C, outline=HEX_C)
    btn_c = tk.Button(window, text="Цвет фона")
    btn_c.config(command=color_cnv)
    btn_c.place(x=1200, y=350)
    def Clear(event=None):
        global HEX, HEX_C, c_state
        state = 0
        scale.set(50)
        HEX = HEX_C
        c_state = 1
    clear = tk.Button(window, text="Стёрка")
    clear.pack()
    clear.config(command=Clear)
    b_all.append(clear)
    def Clear_c(event=None):
        global state, full_path
        full_path=None
        state = 0
        canvas.delete("all")
        open_btn.config(text="Открыть фото")
        window.title("Рисовашка")
    clear_c = tk.Button(window, text="Отчистить")
    clear_c.pack()
    clear_c.config(command=Clear_c)
    b_all.append(clear_c)
    def pickC(event=None):
        global HEX, state, с_state
        state = 0
        с_state = 0
        color = colorchooser.askcolor(title="Выберите цвет кисти")
        if color[1]:
            HEX = color[1]
    def get_Coord(event=None):
        global xw, yw, xs, ys, xc, yc
        xw = window.winfo_rootx()
        yw = window.winfo_rooty()
        xs = window.winfo_pointerx()
        ys = window.winfo_pointery()
        xc = xs - xw - canvas.winfo_x()
        yc = ys - yw - canvas.winfo_y()
    butcol = tk.Button(window, text="Изменить цвет")
    butcol.config(command=pickC)
    butcol.pack()
    label = tk.Label(window, text="Tолщина(в пикселях)")
    label.place(x=20, y=465)
    o_all.append(label)
    b_all.append(label)
    scale = tk.Scale(window, length=300, orient="vertical", from_=100, to=1)
    scale.place(x=50, y=150)
    b_all.append(scale)
    get_Coord()
    oval = long.create_oval(50, 50, 50, 50, fill=None, outline=HEX)
    oval2 = canvas.create_oval(xc - (scale.get() / 2), yc - (scale.get() / 2), xc + (scale.get() / 2), yc + (scale.get() / 2), fill=HEX, outline=HEX)
    def draw(event=None):
        global HEX, clears, c_state, s_state, xc, yc
        get_Coord()
        cursor = "spraycan"
        if HEX != None:
            if canvas.cget("cursor") != cursor:
                canvas.config(cursor=cursor)
            if open_btn.cget("text")[0] != "*":
                open_btn.config(text="*"+open_btn.cget("text"))
            if s_state == 0:
                if c_state == 1:
                    ovl=canvas.create_oval(xc - (scale.get() / 2), yc - (scale.get() / 2), xc + (scale.get() / 2), yc + (scale.get() / 2), fill=HEX, outline=HEX)
                    clears.append(ovl)
                else:
                    canvas.create_oval(xc - (scale.get() / 2), yc - (scale.get() / 2), xc + (scale.get() / 2), yc + (scale.get() / 2), fill=HEX, outline=HEX)
            elif s_state == 1:
                if c_state == 1:
                    rct=canvas.create_rectangle(xc - (scale.get() / 2), yc - (scale.get() / 2), xc + (scale.get() / 2), yc + (scale.get() / 2), fill=HEX, outline=HEX)
                    clears.append(rct)
                else:
                    canvas.create_rectangle(xc - (scale.get() / 2), yc - (scale.get() / 2), xc + (scale.get() / 2), yc + (scale.get() / 2), fill=HEX, outline=HEX)
    def start():
        global oval, oval2, HEX, HEX_C
        butcol.config(bg=HEX)
        btn_c.config(bg=HEX_C)
        long.delete(oval)
        canvas.delete(oval2)
        get_Coord()
        if HEX:
            if s_state == 0:
                oval2 = canvas.create_oval(xc + 2 - (scale.get() / 2), yc + 2 - (scale.get() / 2), xc - 2 +(scale.get() / 2), yc - 2 + (scale.get() / 2), fill=None, outline=HEX, width=2)
                oval = long.create_oval(50 - scale.get()/2, 50 - scale.get()/2, 50 + scale.get()/2, 50 + scale.get()/2, fill=HEX, outline=HEX)
            if s_state == 1:
                oval2 = canvas.create_rectangle(xc + 2 - (scale.get() / 2), yc + 2 - (scale.get() / 2), xc - 2 + (scale.get() / 2), yc - 2 + (scale.get() / 2), fill=None, outline=HEX, width=2)
                oval = long.create_rectangle(50 - scale.get()/2, 50 - scale.get()/2, 50 + scale.get()/2, 50 + scale.get()/2, fill=HEX, outline=HEX)
        elif HEX and (not HEX == "#ffffff"):
            if s_state == 0:
                oval = long.create_oval(50 - scale.get()/2, 50 - scale.get()/2, 50 + scale.get()/2, 50 + scale.get()/2, fill=HEX, outline=HEX)
            if s_state == 1:
                oval = long.create_rectangle(50 - scale.get()/2, 50 - scale.get()/2, 50 + scale.get()/2, 50 + scale.get()/2, fill=HEX, outline=HEX)
        window.after(1, start)
    start()
    def plus(event=None):
        global step
        current = scale.get() + step
        if current < 101:
            scale.set(current)
        if current > 100:
            scale.set(100)
    def minus(event=None):
        current = scale.get() - step
        if current > 0:
            scale.set(current)
        if current < 0:
            scale.set(0)
    def info(event=None):
        w_info = tk.Tk()
        w_info.title("Справка")
        label = tk.Label(w_info, text='1.)Чтобы изменить цвет нажмите на кнопку: "Изменить цвет"\n2.)В правом нижнем углу экрана вы видите обозначение вашей кисти\n3.)Чтобы не рисовать фон вручную нажмите кнопку "Цвет фона"\n4.)Чтобы изменить тему нажмите на кнопу "Тёмная тема/Светлая тема"\nDelete - отчистить\nF1 - выбрать цвет\nF2 - стёрка\nF3 - -толщина\nF4 - +толщина\nF5 - изменить тему\nF6 - выбрать цвет фона\nEsc - хватит\nF7 - справка\nF8 - изменить форму\nF9 - сохранить рисунок\nF10 - открыть фото\nF11 - выбрать раскраску\nShift+F1 - нарисовать линию\nShift+F2 - нарисовать круг\nShift+F3 - нарисовать квадрат\nShift+F4 - сделать текст', font=("Arial", 20))
        label.pack()
        def ok(event=None):
            w_info.destroy()
        inf_btn = tk.Button(w_info, text="Понятно")
        inf_btn.config(command=ok)
        inf_btn.pack()
        w_info.mainloop()
    infoBtn = tk.Button(window, text="Справка")
    infoBtn.config(command=info)
    infoBtn.place(x=1200, y=225)
    b_all.append(infoBtn)
    def shape(event=None):
        global s_state
        if s_state == 0:
            s_state = 1
            shape_btn.config(text="⬤")
        elif s_state == 1:
            s_state = 0
            shape_btn.config(text="⬛")
    shape_btn = tk.Button(window, text="⬛")
    shape_btn.config(command=shape)
    shape_btn.place(x=50, y=50)
    b_all.append(shape_btn)
    def save(event=None):
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        py.moveTo(0, 1000)
        def save_s(event=None):
            image = ImageGrab.grab((x, y, x + width, y + height))
            file_name = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"), ("BMP files", "*.bmp"), ("JPG files", "*.jpg")])
            if file_name != "":
                if "*" in open_btn.cget("text"):
                    open_btn.config(text= open_btn.cget("text").replace("*", "")) 
                image.save(file_name)
        window.after(1000, save_s)
    save_btn = tk.Button(window, text="Сохранить")
    save_btn.place(x=1200, y=0)
    save_btn.config(command=save)
    b_all.append(save_btn)
    def open_img(event=None):
        state = 0
        global photo, full_path
        if open_btn.cget("text")[0] != "*":
            file_path = filedialog.askopenfilename(title="Открыть изображение",filetypes=[("Photo files", "*.bmp;*.png;*.jpg;*.jpeg")])
            if file_path:
                full_path=file_path
                img=Image.open(file_path)
                img=img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
                tk_image=ImageTk.PhotoImage(img)
                photo=tk_image
                canvas.create_image(-2, -1, anchor=tk.NW, image=photo, outline=None)
                open_btn.config(text=os.path.basename(file_path))
                window.title("Рисовашка (" + os.path.basename(file_path) + ")")
                if len(open_btn.cget("text")) > 75:
                    open_btn.config(text=open_btn.cget("text")[:62] + "...")
                    window.title("Рисовашка (" + open_btn.cget("text")[:22] + "...)")
        else:
            sav=tk.Toplevel()
            label=tk.Label(sav, text=f"Сохранить файл {full_path}?")
            label.pack()
            def no(event=None):
                open_btn.config(text=open_btn.cget("text").replace(open_btn.cget("text")[0], ""))
                open_img()
                sav.destroy()
            def yes(event=None):
                x = canvas.winfo_rootx()
                y = canvas.winfo_rooty()
                width = canvas.winfo_width()
                height = canvas.winfo_height()
                image = ImageGrab.grab((x, y, x + width, y + height))
                image.save(full_path)
                open_img()
                sav.destroy()
            savb=tk.Button(sav, text="Сохранить", bg="green", fg="white", command=yes)
            nob=tk.Button(sav, text="Не сохранять", bg="red", fg="white", command=no)
            savb.pack(pady=40, padx=40)
            nob.pack(pady=40, padx=40)
    open_btn = tk.Button(window, text="Открыть фото", wraplength=100)
    open_btn.place(x=1200, y=500)
    open_btn.config(command=open_img)
    b_all.append(open_btn)
    def rainbow(event=None):
        global full_path
        full_path=None
        canvas.create_line(250, 425, 500, 50, 750, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(230, 425, 500, 0, 770, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(210, 425, 500, -50, 790, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(190, 425, 500, -100, 810, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(170, 425, 500, -150, 830, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(150, 425, 500, -200, 850, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(130, 425, 500, -250, 870, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(110, 425, 500, -300, 890, 425, smooth=True, width=10, capstyle="round")
        canvas.create_line(250, 425, 110, 425, width=10, capstyle="round")
        canvas.create_line(750, 425, 890, 425, width=10, capstyle="round")
        state = 0
    def smile(event=None):
        global full_path
        full_path=None
        canvas.create_oval(300, 100, 700, 500, width=10)
        canvas.create_oval(400, 200, 450, 250, width=10)
        canvas.create_oval(550, 200, 600, 250, width=10)
        canvas.create_line(350, 400, 500, 450, 650, 400, smooth=True, width=10, capstyle="round")
        state = 0
    def car(event=None):
        global full_path
        full_path=None
        canvas.create_oval(300, 100, 700, 500, width=10)
        canvas.create_rectangle(290, 250, 710, 510, fill="white", outline="white")
        canvas.create_line(325, 240, 450, 240, 450, 130, width=10, capstyle="round")
        canvas.create_line(325, 240, 355, 140, 450, 130, smooth=True, width=10, capstyle="round")
        canvas.create_line(660, 240, 540, 240, 540, 130, width=10, capstyle="round")
        canvas.create_line(660, 240, 640, 140, 540, 130, smooth=True, width=10, capstyle="round")
        canvas.create_line(500, 100, 500, 300, width=10, capstyle="round")
        canvas.create_line(690, 250, 750, 275, 690, 300, smooth=True, width=10, capstyle="round")
        canvas.create_oval(600, 290, 700, 390, width=10)
        canvas.create_oval(300, 290, 400, 390, width=10)
        canvas.create_line(307, 250, 307, 300, width=10, capstyle="round")
        canvas.create_line(310, 300, 690, 300, width=10, capstyle="round")
        canvas.create_line(325, 270, 345, 270, width=10, capstyle="round")
        canvas.create_line(535, 270, 555, 270, width=10, capstyle="round")
        canvas.create_line(690, 250, 690, 300, width=10, capstyle="round")
        canvas.create_rectangle(257, 270, 307, 280, width=5)
    def none(event=None):
        global full_path
        full_path=None
        x1, y1 = random.randint(0, 1000), random.randint(0, 525)
        x2, y2 = random.randint(0, 1000), random.randint(0, 525)
        x3, y3 = random.randint(0, 1000), random.randint(0, 525)
        x4, y4 = random.randint(0, 1000), random.randint(0, 525)
        x5, y5 = random.randint(0, 1000), random.randint(0, 525)
        x6, y6 = random.randint(0, 1000), random.randint(0, 525)
        x7, y7 = random.randint(0, 1000), random.randint(0, 525)
        x8, y8 = random.randint(0, 1000), random.randint(0, 525)
        x9, y9 = random.randint(0, 1000), random.randint(0, 525)
        canvas.create_line(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x1, y1, width=10, smooth=True, capstyle="round")
    def pickP(event=None):
        pht=tk.Toplevel()
        pht.geometry("300x550")
        pht.title("Выбрать раскраску")
        r = tk.Button(pht, text="Радуга", command=lambda:[canvas.delete("all"), rainbow(), pht.destroy(), open_btn.config(text="Открыть фото"),window.title("Рисовашка")])
        s = tk.Button(pht, text="Улыбка", command=lambda:[canvas.delete("all"), smile(), pht.destroy(), open_btn.config(text="Открыть фото"),window.title("Рисовашка")])
        c = tk.Button(pht, text="Машина", command=lambda:[canvas.delete("all"), car(), pht.destroy(), open_btn.config(text="Открыть фото"),window.title("Рисовашка")])
        n = tk.Button(pht, text="Чёрти-что", command=lambda:[canvas.delete("all"), none(), pht.destroy(), open_btn.config(text="Открыть фото"),window.title("Рисовашка")])
        r.pack(pady=50)
        s.pack(pady=50)
        c.pack(pady=50)
        n.pack(pady=50)
        pht.mainloop()
    photo_btn=tk.Button(window, text="Выбрать раскраску")
    photo_btn.pack()
    photo_btn.config(command=pickP)
    b_all.append(photo_btn)
    def line(event=None):
        global l, open_
        open_=True
        x1=None
        y1=None
        x2=None
        y2=None
        l=canvas.create_line(-10, -10, -10, -10)
        def update_line():
            global x1, y1, l, open_
            if not open_:
                return
            pos=py.position()
            x=pos.x-canvas.winfo_rootx()
            y=pos.y-canvas.winfo_rooty()
            if l is not None:
                canvas.delete(l)
                l=None
            l=canvas.create_line(x1, y1, x, y, fill=HEX, width=2)
            if open_:
                window.after(1, update_line)
        def coord1(event=None):
            global x1, y1
            pos=py.position()
            x1=pos.x-canvas.winfo_rootx()
            y1=pos.y-canvas.winfo_rooty()
            update_line()
        def coord2(event=None):
            global x1, y1, x2, y2, HEX, open_, l
            open_=False
            pos=py.position()
            x2=pos.x-canvas.winfo_rootx()
            y2=pos.y-canvas.winfo_rooty()
            canvas.delete(l)
            canvas.create_line(x1, y1, x2, y2, width=scale.get(), fill=HEX, capstyle="round")
            canvas.unbind("<Button-1>")
            canvas.unbind("<ButtonRelease-1>")
            canvas.bind("<B1-Motion>", draw)
            canvas.bind("<Button-1>", draw)
            canvas.bind("<ButtonRelease-1>", arrow)
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<Button-1>")
        canvas.unbind("<ButtonRelease-1>")
        canvas.bind("<Button-1>", coord1)
        canvas.bind("<ButtonRelease-1>", coord2)
    def oval(event=None):
        global o, open_
        open_=True
        x1=None
        y1=None
        x2=None
        y2=None
        o=canvas.create_oval(-100, -100, -100, -100, outline=HEX, width=2)
        def update_oval():
            global x1, y1, o, open_
            if not open_:
                return
            pos=py.position()
            x=pos.x-canvas.winfo_rootx()
            y=pos.y-canvas.winfo_rooty()
            if o is not None:
                canvas.delete(o)
                o=None
            o=canvas.create_oval(x1, y1, x, y, outline=HEX, width=2)
            if open_:
                window.after(1, update_oval)
        def coord1(event=None):
            global x1, y1
            pos=py.position()
            x1=pos.x-canvas.winfo_rootx()
            y1=pos.y-canvas.winfo_rooty()
            update_oval()
        def coord2(event=None):
            global x1, y1, x2, y2, HEX, open_, o
            open_=False
            pos=py.position()
            x2=pos.x-canvas.winfo_rootx()
            y2=pos.y-canvas.winfo_rooty()
            canvas.delete(o)
            canvas.create_oval(x1, y1, x2, y2, outline=HEX, fill=HEX)
            canvas.unbind("<Button-1>")
            canvas.unbind("<ButtonRelease-1>")
            canvas.bind("<B1-Motion>", draw)
            canvas.bind("<Button-1>", draw)
            canvas.bind("<ButtonRelease-1>", arrow)
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<Button-1>")
        canvas.unbind("<ButtonRelease-1>")
        canvas.bind("<Button-1>", coord1)
        canvas.bind("<ButtonRelease-1>", coord2)
    def rect(event=None):
        global r, open_
        open_=True
        x1=None
        y1=None
        x2=None
        y2=None
        r=canvas.create_rectangle(-100, -100, -100, -100, outline=HEX, width=2)
        def update_rect():
            global x1, y1, r, open_
            if not open_:
                return
            pos=py.position()
            x=pos.x-canvas.winfo_rootx()
            y=pos.y-canvas.winfo_rooty()
            if r is not None:
                canvas.delete(r)
                r=None
            r=canvas.create_rectangle(x1, y1, x, y, outline=HEX, width=2)
            if open_:
                window.after(1, update_rect)
        def coord1(event=None):
            global x1, y1
            pos=py.position()
            x1=pos.x-canvas.winfo_rootx()
            y1=pos.y-canvas.winfo_rooty()
            update_rect()
        def coord2(event=None):
            global x1, y1, x2, y2, HEX, open_, r
            open_=False
            pos=py.position()
            x2=pos.x-canvas.winfo_rootx()
            y2=pos.y-canvas.winfo_rooty()
            canvas.delete(r)
            canvas.create_rectangle(x1, y1, x2, y2, outline=HEX, fill=HEX)
            canvas.unbind("<Button-1>")
            canvas.unbind("<ButtonRelease-1>")
            canvas.bind("<B1-Motion>", draw)
            canvas.bind("<Button-1>", draw)
            canvas.bind("<ButtonRelease-1>", arrow)
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<Button-1>")
        canvas.unbind("<ButtonRelease-1>")
        canvas.bind("<Button-1>", coord1)
        canvas.bind("<ButtonRelease-1>", coord2)
    def text(event=None):
        global HEX
        t_w=tk.Toplevel(window)
        def update_font(event=None):
            label.config(font=(font.get(), label.cget("font").split()[1]))
        def update_size(event=None):
            label.config(font=(label.cget("font").split()[0], size.get()))
        def update_text(event=None):
            label.config(text=entry.get())
            if t_w.winfo_exists():
                t_w.after(10, update_text)
        def update_text_on_canvas(event=None):
            s=canvas.bbox(text)[2]-canvas.bbox(text)[0], canvas.bbox(text)[3]-canvas.bbox(text)[1]
            x=py.position().x-canvas.winfo_rootx()-s[0]/2
            y=py.position().y-canvas.winfo_rooty()-s[1]/2
            canvas.moveto(text, x, y)
            canvas.itemconfig(text, text=entry.get(), font=(font.get(), size.get()))
            if t_w.winfo_exists():
                t_w.after(10, update_text_on_canvas)
        entry=tk.Entry(t_w)
        entry.pack()
        label=tk.Label(t_w, text="Предпросмотр", font=("Arial", 12), fg=HEX)
        label.pack()
        font=tk.StringVar(window)
        size=tk.IntVar(window)
        sizes=range(7, 41)
        fonts=['System', 'Terminal', 'Fixedsys', 'Modern', 'Roman', 'Script', 'Courier', 'Marlett', 'Arial', 'Bahnschrift', 'Calibri', 'Cambria', 'Candara', 'Consolas', 'Constantia', 'Corbel', 'Courier', 'Ebrima', 'Gabriola', 'Gadugi', 'Georgia', 'Impact', 'MingLiU-ExtB', 'PMingLiU-ExtB', 'MingLiU_HKSCS-ExtB', 'SimSun', 'NSimSun', 'Sylfaen', 'Symbol', 'Tahoma', 'Verdana', 'Webdings', 'Wingdings', 'Century', 'Algerian', 'Broadway', 'Centaur', 'Chiller', 'Harrington', 'Jokerman', 'Magneto', 'Mistral', 'Onyx', 'Parchment', 'Playbill', 'Ravie', 'Stencil', 'Vivaldi', 'Rockwell', 'Pristina', 'Perpetua', 'Papyrus', 'Haettenschweiler', 'Gigi', 'Garamond', 'Forte', 'Elephant', 'Castellar', 'Dubai', 'Shell']
        font.set("Arial")
        size.set(12)
        font_w=tk.OptionMenu(t_w, font, *fonts, command=update_font)
        font_w.pack()
        size_w=tk.OptionMenu(t_w, size, *sizes, command=update_size)
        size_w.pack()
        text=canvas.create_text(100, 100, text=entry.get(), font=(font.get(), size.get()), fill=HEX)
        update_text()
        update_text_on_canvas()
        def place_text(event=None):
            global HEX
            x=py.position().x-canvas.winfo_rootx()
            y=py.position().y-canvas.winfo_rooty()
            canvas.create_text(x, y, text=entry.get(), font=(font.get(), size.get()), fill=HEX)
            canvas.delete(text)
            t_w.destroy()
            canvas.unbind("<Button-1>")
            canvas.bind("<Button-1>", draw)
        canvas.unbind("<Button-1>")
        canvas.bind("<Button-1>", place_text)
        t_w.mainloop()
    def stay_or_close(event=None):
        global full_path, label
        if open_btn.cget("text")[0] == "*":
            stay_or_close_w = tk.Toplevel()
            stay_or_close_w.grab_set()
            stay_or_close_w.geometry("400x400")
            stay_or_close_w.title("Сохранить?")
            if full_path != None:
                label = tk.Label(stay_or_close_w, text=f"Сохранить изменения в файле\n{full_path}?", wraplength=250)
                if len(label.cget("text")) > 119:
                    label.config(text=label.cget("text").replace("?", "")[:119] + "...?", wraplength=250)
            else:
                label = tk.Label(stay_or_close_w, text="Сохранить файл\nбезымянный?")
            label.pack()
            s=tk.Button(stay_or_close_w, text="Coхpaнить", bg="green", fg="white")
            c=tk.Button(stay_or_close_w, text="Не сохранять", bg="red", fg="white")
            n=tk.Button(stay_or_close_w, text="Отмена", bg="blue", fg="white")
            s.pack(pady=40)
            c.pack(pady=40)
            n.pack(pady=40)
            def save(event=None):
                global full_path, label
                py.moveTo(0, 1000)
                def ok_save():
                    x = canvas.winfo_rootx()
                    y = canvas.winfo_rooty()
                    width = canvas.winfo_width()
                    height = canvas.winfo_height()
                    img = ImageGrab.grab((x, y, x + width, y + height))
                    if full_path != None:
                        img.save(full_path)
                    else:
                        file_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"), ("BMP files", "*.bmp"), ("JPG files", "*.jpg")])
                        if file_path != "":
                            img.save(file_path)
                    window.destroy()
                window.after(1000, ok_save)
                stay_or_close_w.destroy()
            c.config(command=lambda:[stay_or_close_w.destroy(), window.destroy()])
            n.config(command=lambda:stay_or_close_w.destroy())
            s.config(command=save)
            stay_or_close_w.mainloop()
        else:
            window.destroy()
    def arrow(event=None):
        canvas.config(cursor="tcross")
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<Button-1>", draw)
    canvas.bind("<ButtonRelease-1>", arrow)
    window.bind("<Delete>", Clear_c)
    window.bind("<F1>", pickC)
    window.bind("<F2>", Clear)
    window.bind("<F3>", minus)
    window.bind("<F4>", plus)
    window.bind("<F5>", bg_c)
    window.bind("<F6>", color_cnv)
    window.bind("<Escape>", stay_or_close)
    window.bind("<F7>", info)
    window.bind("<F8>", shape)
    window.bind("<F9>", save)
    window.bind("<F10>", open_img)
    window.bind("<F11>", pickP)
    window.bind("<Shift-F1>", line)
    window.bind("<Shift-F2>", oval)
    window.bind("<Shift-F3>", rect)
    window.bind("<Shift-F4>", text)
    window.protocol("WM_DELETE_WINDOW", stay_or_close)
    window.mainloop()
label = tk.Label(w_info, text='1.)Чтобы изменить цвет нажмите на кнопку: "Изменить цвет"\n2.)В правом нижнем углу экрана вы видите обозначение вашей кисти\n3.)Чтобы не рисовать фон вручную нажмите кнопку "Цвет фона"\n4.)Чтобы изменить тему нажмите на кнопу "Тёмная тема/Светлая тема"\nDelete - отчистить\nF1 - выбрать цвет\nF2 - стёрка\nF3 - -толщина\nF4 - +толщина\nF5 - изменить тему\nF6 - выбрать цвет фона\nEsc - хватит\nF7 - справка\nF8 - изменить форму\nF9 - сохранить рисунок\nF10 - открыть фото\nF11 - выбрать раскраску\nShift+F1 - нарисовать линию\nShift+F2 - нарисовать круг\nShift+F3 - нарисовать квадрат\nShift+F4 - сделать текст', font=("Arial", 20))
label.pack()
inf_btn = tk.Button(w_info, text="Понятно")
inf_btn.config(command=START)
inf_btn.pack()
w_info.bind("<F5>", START)
w_info.mainloop()
