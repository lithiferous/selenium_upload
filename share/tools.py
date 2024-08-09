import config
import openpyxl
import os
import pandas as pd
import pyautogui as pgui
import time
from elements import SmartElement
from conditions import visible
from openpyxl import load_workbook
from tkinter import Tk

def add(element, text):
    return s(element).assure(visible).left_click().set_value(text)

def css(css_selector_name):
    return pd.read_pickle(os.getcwd()+"/core/share/css.pkl").get(css_selector_name)

def edit_form(element, text):
    return s(element).assure(visible).left_click().s(element).set_value(text)

def goto(element):
    return s(element).assure(visible).left_click()

def s(css_selector):
    return SmartElement(css_selector, config.browser)

def send_files(zipfilepath):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(zipfilepath)
    r.update()
    time.sleep(1.5)
    pgui.hotkey('ctrl', 'v')
    time.sleep(3.5)
    pgui.press('enter')
    time.sleep(3.5)
    pgui.press('enter')
    r.destroy()

def write_share_info(folder, element, rtb_platform, id_list, campaign, period):
    id_list = id_list if id_list is not None else []
    campaign = campaign if campaign is not None else None
    period = period if period is not None else None

    add_text = ""
    if campaign:
        add_text +="Компания: " + campaign + "\n"
    if period:
        add_text +="Даты РК: " + period + "\n"
    if id_list:
        id_list = [_id.strip() for _id in id_list[0].split(',')]
        add_text +="id баннеров: " + ", ".join(id_list) + "\nСсылка: "
    else:
        add_text += "Ссылка: "

    url = s(element).assure(visible).get_value("value")
    _file = folder + "/logs/share_info_" + rtb_platform + '.txt'
    with open(_file, "w+") as f:
        f.write(add_text + url)
        f.write("\nПароль: 0000\n")
    s(element).press_esc()

def upload_finish(element):
    try:
        s(element).assure(visible)
        time.sleep(15)
    except:
        pass

def visit(url):
    config.browser.get(url)

