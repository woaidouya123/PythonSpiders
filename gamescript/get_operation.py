import PyHook3
import pythoncom
from PyHook3.HookManager import GetKeyState
from PyHook3.HookManager import HookConstants
import sys
import win32api
import time

# 创建管理器
hm = PyHook3.HookManager()
saved_op = []
begin_time = None
is_recording = False

# 监听到鼠标事件调用
def onMouseEvent(event):
    global begin_time
    cur_time = time.time()
    saved_op.append({
        'type':'wait',
        'time':cur_time - begin_time
        })
    saved_op.append({
        'type':'click',
        'position':event.Position
        })
    begin_time = cur_time
    return True

# 监听到键盘事件调用
def onKeyboardEvent(event):
    global begin_time
    ctrl_pressed = GetKeyState(HookConstants.VKeyToID('VK_CONTROL'))
    if(ctrl_pressed and event.Key == 'P'):
        global is_recording
        is_recording = False
        hm.UnhookKeyboard()
        hm.UnhookMouse()
        win32api.PostQuitMessage()
    cur_time = time.time()
    saved_op.append({
        'type':'wait',
        'time':cur_time - begin_time
        })
    saved_op.append({
        'type':'keydown',
        'key':event.Key
        })
    begin_time = cur_time
    return True

def getRecord():
    return saved_op

def stop():
    global is_recording
    is_recording = False
    hm.UnhookKeyboard()
    hm.UnhookMouse()
    win32api.PostQuitMessage()

def start():
    global begin_time,is_recording
    is_recording = True
    saved_op = []
    delay = 3
    # 监听键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 监听鼠标 
    hm.MouseLeftUp = onMouseEvent
    hm.HookMouse()
    
    # 循环监听
    begin_time = time.time()
    pythoncom.PumpMessages()

