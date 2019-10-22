import sys
from os import listdir
from os.path import join

from PyQt5.QtWidgets import QDockWidget, QPushButton, QSplitter, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from util.message import LOADDATA, LOADDATAFAIL, LOADDATASUCCESS, SEGMENTATION, OPTIONALPLAN, ERROR


class ChildWindow(QDockWidget):
    signal_id = pyqtSignal(name='id') # 加载ID
    signal_load_data = pyqtSignal(str, name='objectChanged') # 加载数据信号
    signal_pre = pyqtSignal(name='pre_video')   # 上一个信号
    signal_next = pyqtSignal(name='next_video')   # 后一个信号
    signal_description = pyqtSignal(name='description') # 描述信号
    signal_class = pyqtSignal(name='class') # 类别信号

    def __init__(self, title='Child Window'):
        QDockWidget.__init__(self, title)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # --------------------定义三个按钮
        self.in_id = QPushButton('ID')
        self.loadDataBtn = QPushButton('导入视频 L')
        self.loadDataBtn.setShortcut('L')
        self.pre_Btn = QPushButton('前一个 W')
        self.pre_Btn.setShortcut('W')
        self.next_Btn = QPushButton('后一个 S')
        self.next_Btn.setShortcut("S")
        self.descri_Btn = QPushButton('描述视频 D')
        self.class_Btn = QPushButton('类别 C')
        self.class_Btn.setShortcut('C')


        # --------------------按钮点击事件
        self.in_id.clicked.connect(self.btn_in_id)
        self.loadDataBtn.clicked.connect(self.btn_load_clicked)
        self.pre_Btn.clicked.connect(self.btn_pre_clicked)
        self.next_Btn.clicked.connect(self.btn_next_clicked)
        self.descri_Btn.clicked.connect(self.btn_description_clicked)
        self.class_Btn.clicked.connect(self.btn_class)

        # --------------------将组件加入副窗口
        splitter_v = QSplitter(Qt.Vertical)
        splitter_v.addWidget(self.in_id)
        splitter_v.addWidget(self.loadDataBtn)
        splitter_v.addWidget(self.pre_Btn)
        splitter_v.addWidget(self.next_Btn)
        splitter_v.addWidget(self.class_Btn)
        splitter_v.addWidget(self.descri_Btn)
        self.setWidget(splitter_v)


    # --------------------导入数据按钮点击事件

    def btn_load_clicked(self):
        file_path = self.openfile()
        if self.testFile(file_path) == False:
            self.signal_load_data.emit(ERROR)
        else:
            self.signal_load_data.emit(file_path)
        pass

    # --------------------前一个
    def btn_pre_clicked(self):
        self.signal_pre.emit()
        pass

    # --------------------后一个
    def btn_next_clicked(self):
        self.signal_next.emit()
        pass

    # --------------------手术方案按钮点击事件
    def btn_description_clicked(self):
        self.signal_description.emit()
        pass

    # --------------------输入ID按钮
    def btn_in_id(self):
        self.signal_id.emit()
        pass

    # --------------------打开文件
    def openfile(self):
        file_path, _ = QFileDialog.getOpenFileName(self)
        return file_path

    # --------------------输入类别按钮
    def btn_class(self):
        self.signal_class.emit()
        pass

    # --------------------测试文件是否为raw
    def testFile(self, filename):
        return any(filename.endswith(extension) for extension in [".mp4"])
