import PyHook3
import pythoncom
from PyHook3.HookManager import GetKeyState
from PyHook3.HookManager import HookConstants
import sys
import win32api

# 创建管理器
hm = PyHook3.HookManager()

# 监听到鼠标事件调用
def onMouseEvent(event):
    if(event.MessageName!="mouse move"):
        print(event.MessageName)
    return True

# 监听到键盘事件调用
def onKeyboardEvent(event):
    print(event.Key)# 返回按下的键
    ctrl_pressed = GetKeyState(HookConstants.VKeyToID('VK_CONTROL'))
    if(ctrl_pressed and event.Key == 'P'):
        hm.UnhookKeyboard()
        hm.UnhookMouse()
        win32api.PostQuitMessage()
    return True

def main():
    # 监听键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 监听鼠标 
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    # 循环监听
    pythoncom.PumpMessages()

 
if __name__ == "__main__":
    main()
