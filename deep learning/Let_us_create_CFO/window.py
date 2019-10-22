import os
import sys
from datetime import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QMutex, QMutexLocker
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QSplitter, QApplication, QStyle, QLabel, QPushButton, \
    QHBoxLayout, QVBoxLayout, QToolBar, QLineEdit, QFormLayout, QTextEdit, QMessageBox
from _thread import start_new_thread

from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_GRAY2BGR, VideoCapture, CAP_PROP_FPS


from ChildWindow import ChildWindow
from DataManage import DataMange
from util.message import LOADDATAFAIL, LOADDATASUCCESS, ERROR, WELCOME, SEGMENTATION, SEGMENTATIONSUCCESS, OPTIONALPLAN, \
    OPTIONALPLANSUCCESS, OPTIONALPLANFAIL


# ---------------------------------------- 主窗口 ----------------------------------------
from videobox import VideoBox


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.msg = WELCOME
        self.dataManage = DataMange()
        self.mainWindow()

    def mainWindow(self):
        # 副窗口
        self.childwidget = ChildWindow('操作栏')
        self.childwidget.signal_id.connect(self.in_id)
        # 获得视频
        self.childwidget.signal_load_data.connect(self.load_data)
        # 下一个视频
        self.childwidget.signal_next.connect(self.next_video)
        # 上一个视频
        self.childwidget.signal_pre.connect(self.pre_video)
        # 填写描述
        self.childwidget.signal_description.connect(self.description)
        # 填写类别
        self.childwidget.signal_class.connect(self.in_class)

        # 场景盒子
        self.view_box = VideoBox()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.view_box)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.childwidget)
        self.setCentralWidget(splitter)

        self.setGeometry(200, 200, 800, 400)
        self.setWindowTitle('Let us create CFO!')
        self.setWindowIcon(QIcon('logo\\logo.jpg'))

        toolbar = QToolBar()

        self.btn_save = QPushButton('保存')
        self.btn_save.clicked.connect(self.save)

        self.message = QLabel()

        toolbar.addWidget(self.btn_save)
        toolbar.addWidget(self.message)
        self.addToolBar(Qt.BottomToolBarArea, toolbar)

        self.build_message_toolbar()
        self.addToolBar(Qt.RightToolBarArea, self.toolbar_massage)
        self.init_message()

    def init_message(self):
        if self.dataManage.file_path_now != 1024:
            (dirname, filename) = os.path.split(self.dataManage.file_path_now)
        else:
            filename = None
        self.ID.setText('ID: '+ str(self.dataManage.id))
        self.name.setText('视频名称: '+ str(filename))
        self.class_.setText('视频类别: '+ str(self.dataManage.class_))
        self.discription.setText('描述: '+ str(self.dataManage.description))

    def build_message_toolbar(self):
        self.toolbar_massage = QToolBar()
        # 创建4个单行文本框
        self.name = QLineEdit()
        # 设置输入文本右对齐
        self.class_ = QLineEdit()
        self.ID = QLineEdit()
        self.discription = QLineEdit()

        self.name.setReadOnly(True)
        self.ID.setReadOnly(True)
        self.discription.setReadOnly(True)
        self.class_.setReadOnly(True)

        # 把文本框添加到布局，第一个参数为左侧的说明标签
        self.toolbar_massage.addWidget(self.ID)
        self.toolbar_massage.addWidget(self.name)
        self.toolbar_massage.addWidget(self.class_)
        self.toolbar_massage.addWidget(self.discription)

    def save(self):
        is_save = self.dataManage.save()
        if is_save:
            if self.dataManage.file_path_now != None:
                (dirname, filename) = os.path.split(self.dataManage.file_path_now)
            else:
                filename = None
            self.message.setText(str(filename) + '保存 成功')
            self.init_message()
        else:
            if self.dataManage.file_path_now != None:
                (dirname, filename) = os.path.split(self.dataManage.file_path_now)
            else:
                filename = None
            self.message.setText(str(filename) + '保存 失败')
            QMessageBox.question(self, 'Message', '存在未填写项', QMessageBox.Yes)


    def in_id(self):
        value, ok = QInputDialog.getText(self, "输入ID", str(self.dataManage.get_id()))
        if ok and value:
            self.dataManage.set_id(value)
            self.init_message()
        else:
            self.msg = OPTIONALPLANFAIL
        pass

    def in_class(self):
        value, ok = QInputDialog.getText(self, "输入类别", str(self.dataManage.get_class()))
        if ok and value:
            self.dataManage.set_class(value)
            self.init_message()
        else:
            self.msg = OPTIONALPLANFAIL
        pass

    def load_data(self, file_path):
        try:
            start_new_thread(self.thread_load_data, (file_path,))
        except:
            print("Error: unable to start thread")
        pass

    def description(self):
        value, ok = QInputDialog.getMultiLineText(self, "视频描述", "请对该视频的描述：")
        if ok and value:
            self.dataManage.set_description(value)
            self.init_message()
        else:
            self.msg = OPTIONALPLANFAIL
        pass

    def next_video(self):
        try:
            start_new_thread(self.thread_do_next, ())

        except:
            print("Error: unable to start thread")
        pass

    def pre_video(self):
        try:
            start_new_thread(self.thread_do_pre, ())
        except:
            print("Error: unable to start thread")
        pass

    def thread_load_data(self, file_path):
        if file_path == ERROR:

            print("Error: Wrong path")
        else:
            self.dataManage.file_data_now(file_path)
            self.view_box.video_url = file_path
            self.view_box.reset()
            self.view_box.playCapture.release()
            self.init_message()
        pass

    def thread_do_next(self):
        file_next_path = self.dataManage.file_next()
        self.view_box.video_url = file_next_path
        self.view_box.reset()
        self.view_box.playCapture.release()
        self.init_message()
        pass

    def thread_do_pre(self):
        file_pre_path = self.dataManage.file_pre()
        self.view_box.video_url = file_pre_path
        self.view_box.reset()
        self.view_box.playCapture.release()
        self.init_message()
        pass




def main():
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QPushButton{
            
            min-width: 6em;
            max-width: 6em;
        }
        QPushButton#cancel{
            background-color: red ;
        }
        ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()