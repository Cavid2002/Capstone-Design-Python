import multiprocessing
from tkinter import *
from math import *
import multiprocessing
import subprocess
from threaded_client import client_start


app = Tk()
output_text: str = ""
screen: Label = None
my_font = ("",18,'bold')

# ----------action listner--------------
def delete_onclick() -> None:
    global output_text,screen
    output_text = output_text[:-1]
    screen.config(text = output_text)

def delete_all_onclick() -> None:
    global output_text,screen
    output_text = ""
    screen.config(text = output_text)

def click_listner(val: str) -> None:
    global output_text,screen
    output_text = output_text + str(val)
    screen.config(text = output_text)

def equal_listner() -> None:
    global output_text,screen
    try:
        res = eval(output_text)
        output_text = str(res)
    except:
        output_text = "ERROR"
    screen.config(text=output_text)

def adv_click_listner(val: str) -> None:
    global output_text,screen
    line: str = val + "(radians(" + output_text + "))"
    output_text = line
    screen.config(text=output_text)


def pow_click_listner(val: str) -> None:
    global output_text,screen
    line: str = val + "(" + output_text + ")"
    output_text = line
    screen.config(text=output_text)


#-------------GUI Elements---------------
def add_oper_buttons(app: Tk) -> None:
    opp_btns: Button = [None] * 4
    trig_opp_btns: Button = [None] * 4
    pow_opp_btns: Button = [None] * 4
    pow_opp = ["sqrt", "log10", "log2", "log"]
    opp = ["+","-","*","/"]
    trig_opp = ["sin", "cos", "tan", "cot"]
    euler: Button = Button(app, text = "e", width = 4, height = 2,
                     command = lambda a = e: click_listner(a),
                     background="orange",font = my_font)
    euler.grid(row = 5, column = 5,padx = 2,pady = 2,stick="wens")
    for i in range(0,4):
        pow_opp_btns[i] = Button(app, text = pow_opp[i], width = 4, height = 2,
                     command = lambda a = pow_opp[i]: pow_click_listner(a),
                     background="orange",font = my_font)
        pow_opp_btns[i].grid(row = i + 1, column = 5,padx = 2,pady = 2,stick="wens")

    for i in range(0,4):
        trig_opp_btns[i] = Button(app, text = trig_opp[i], width = 4, height = 2,
                     command = lambda a = trig_opp[i]: adv_click_listner(a),
                     background="orange",font = my_font)
        trig_opp_btns[i].grid(row = i + 1, column = 4,padx = 2,pady = 2,stick="wens")
    
    pi_btn: Button = Button(app, text = "π", width = 4, height = 2,
                     command = lambda a = pi: click_listner(a),
                     background="orange",font = my_font)
    pi_btn.grid(row = 5, column = 4,padx = 2,pady = 2,stick="wens")
    
    for i in range(0,4):
        opp_btns[i] = Button(app, text = opp[i], width = 4, height = 2,
                     command = lambda a = opp[i]: click_listner(a),
                     background="orange",font = my_font)
        opp_btns[i].grid(row = i + 1, column = 3,padx = 2,pady = 2,stick="wens")
    equal =  Button(app, text = '=', width = 4, height = 2,
                    command = equal_listner,
                    background="orange",font = my_font)
    equal.grid(row=5,column=0,columnspan=2,stick="wens",padx = 2,pady = 2)


def add_num_buttons(app: Tk) -> None:
    global output_text
    num_btns: Button = [None] * 10
    c: int = 1
    num_btns[0] = Button(app, text ="0", width = 4, height = 2,
                     command = lambda a = 0: click_listner(a),
                     background="orange",font = my_font)
    num_btns[0].grid(row = 4,column = 0,padx = 2,pady = 2,stick="wens")
    for i in range(1,4):
        for j in range(0,3):
            num_btns[c] = Button(app, text = f"{c}", width = 4, height = 2,
                             command = lambda a = c: click_listner(a),
                             background="orange",font = my_font)
            num_btns[c].grid(row = i, column = j,padx = 2,pady = 2,stick="wens")
            c = c + 1
    dot = Button(app, text =".", width = 4, height = 2,
                     command = lambda a = ".": click_listner(a),
                     background="orange",font = my_font)
    dot.grid(row = 4,column = 1,columnspan=2,stick="wens",padx = 2,pady = 2)

def add_del_buttons(app: Tk) -> None:
    del_btn = Button(app, text ="C", width = 4, height = 2,
                     command = delete_onclick,
                     background="orange",font = my_font)
    del_btn.grid(row=5,column=3,padx = 2,pady = 2,stick="wens")
    del_all_btn = Button(app, text ="AC", width = 4, height = 2,
                     command = delete_all_onclick,
                     background="orange",font = my_font)
    del_all_btn.grid(row=5,column=2,padx = 2,pady = 2,stick="wens")
    
    
def create_output_screen() -> None:
    global screen
    global app
    screen = Label(app, text = output_text, height = 2,width=5,
                   font = my_font,justify="left",anchor = "nw",
                   borderwidth = 2, relief = "groove",
                   background = "#4f4f4f",
                   foreground="white")
    screen.grid(column = 0, row = 0, columnspan = 6,stick="wens")

def grid_config(app: Tk):
    for i in range(0,6):
        app.grid_columnconfigure(i,weight=1)
    for i in range(0,6):
        app.grid_rowconfigure(i,weight=1)

#---------Entry point---------------
if __name__ == '__main__':
    p = multiprocessing.Process(target=client_start)
    p.start()
    app.geometry("450x500")
    app.minsize(400,400)
    app.title("Basic Calculator")
    app.config(background = "#4f4f4f")
    create_output_screen()
    grid_config(app)
    add_num_buttons(app)
    add_oper_buttons(app)
    add_del_buttons(app)
    app.mainloop()
    

