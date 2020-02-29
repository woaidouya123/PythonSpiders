import sys
from PyQt5.QtWidgets import QApplication,QToolTip, QPushButton, QWidget, QMessageBox, QDesktopWidget,QLabel,QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
import get_operation as GetOp
import repeat_operation as RepOp
import time
 
 
class AutoGame(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI() #界面绘制交给InitUi方法
        
        
    def initUI(self):
        # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        QToolTip.setFont(QFont('SansSerif', 10))
        
        #创建一个PushButton并为他设置一个tooltip
        btn_start = QPushButton('Start', self)
        # btn_start.setToolTip('This is a <b>QPushButton</b> widget')
        btn_start.clicked.connect(self.record_start)
        btn_start.resize(btn_start.sizeHint())

        btn_stop = QPushButton('Stop', self)
        # btn_stop.setToolTip('This is a <b>QPushButton</b> widget')
        btn_stop.clicked.connect(self.record_stop)
        btn_stop.resize(btn_stop.sizeHint())
        btn_stop.move(100,0)

        btn_repeat = QPushButton('Repeat', self)
        # btn_repeat.setToolTip('This is a <b>QPushButton</b> widget')
        btn_repeat.clicked.connect(self.record_repeat)
        btn_repeat.resize(btn_repeat.sizeHint())
        btn_repeat.move(200,0)

        self.lbl = QLabel(self)
        self.lbl.move(0, 40)

        #设置窗口大小
        self.resize(300, 200)
        self.center()
        #设置窗口的标题
        self.setWindowTitle('script') 
        
        #显示窗口
        self.show()
        # 当前选中的录制操作
        self.cur_record = []
        self.delay = 3
    # button点击事件
    def record_start(self):
        delay = self.delay
        while delay > 0:
            print("{}秒后开始记录键鼠操作".format(delay))
            self.change_text("{}秒后开始记录键鼠操作".format(delay))
            delay = delay -1
            time.sleep(1)
        self.change_text("开始录制，点击Stop或者组合键ctrl+p结束录制")
        GetOp.start()
        self.cur_record = GetOp.getRecord()
        self.change_text("录制已完成")
        print(self.cur_record)
    def record_stop(self):
        GetOp.stop()
    def record_repeat(self):
        if(len(self.cur_record) <= 0):
            reply = QMessageBox.warning(self, '提示',
            "请先录制脚本！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            RepOp.repeat(self.cur_record, 1)

    def change_text(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    #控制窗口显示在屏幕中心的方法    
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
 
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  

if __name__ == '__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = AutoGame()
    sys.exit(app.exec_()) 