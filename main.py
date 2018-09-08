from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog

import tcp_logic, udp_logic, web_logic
import socket
import sys
import binascii

from callscan import MyDialog
from constant import Constant


class MainWindow(tcp_logic.TcpLogic, udp_logic.UdpLogic, web_logic.WebLogic):

    def __init__(self, num):
        super(MainWindow, self).__init__(num)
        self.client_socket_list = list()
        self.another = None
        self.link = False
        # 初始化的时候加载bin文件 存储在这个数组里面
        self.arrs = []
        self.setWindowIcon(QIcon("image/b.png"))
        # 打开软件时默认获取本机ip
        self.get_ip()
        self.setWindowFlags(QtCore.Qt.Window)




    def get_ip(self):
        self.lineEdit_ip_local.clear()
        my_addr = socket.gethostbyname(socket.gethostname())
        self.lineEdit_ip_local.setText(str(my_addr))

    def connect(self, ):
        """
        控件信号-槽的设置
        :param : QDialog类创建的对象
        :return: None
        """
        # 如需传递参数可以修改为connect(lambda: self.click(参数))
        super(MainWindow, self).connect()
        self.pushButton_link.clicked.connect(self.click_link)
        self.pushButton_unlink.clicked.connect(self.click_unlink)
        self.pushButton_get_ip.clicked.connect(self.click_get_ip)
        self.pushButton_clear.clicked.connect(self.click_clear)
        self.pushButton_send.clicked.connect(self.send)
        self.pushButton_dir.clicked.connect(self.click_dir)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_else.clicked.connect(self.another_window)
        self.label_written.clicked.connect(self.load_file)
        self.pushButton_reset_all.clicked.connect(self.show_confirm_message)



    def load_file(self):
        print("加载文件")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            print(filenames[0])
            self.read_bin(filenames[0])


    def click_link(self):
        """
        pushbutton_link控件点击触发的槽
        :return: None
        """
        # 连接时根据用户选择的功能调用函数
        if self.comboBox_tcp.currentIndex() == 0:
            self.tcp_server_start()
        if self.comboBox_tcp.currentIndex() == 1:
            self.tcp_client_start()
        if self.comboBox_tcp.currentIndex() == 2:
            self.udp_server_start()
        if self.comboBox_tcp.currentIndex() == 3:
            self.udp_client_start()
        if self.comboBox_tcp.currentIndex() == 4:
            self.web_server_start()


    def click_unlink(self):
        """
        pushbutton_unlink控件点击触发的槽
        :return: None
        """
        # 关闭连接
        self.close_all()
        self.link = False
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def click_get_ip(self):
        """
        pushbutton_get_ip控件点击触发的槽
        :return: None
        """
        # 获取本机ip
        # self.lineEdit_ip_local.clear()
        # my_addr = socket.gethostbyname(socket.gethostname())
        # self.lineEdit_ip_local.setText(str(my_addr))
        self.slotInformation()

    def slotInformation(self):
        reply = QMessageBox.question(self, '提示', '确认现在对云台进行更新?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.combox_port_select.currentText() == "all connections":
                reply_in = QMessageBox.question(self, '提示', '没有选择端口', QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply_in ==QMessageBox.Yes:
                    return
                    pass
                else:
                    return
                    pass
            self.tcp_send(init_code=Constant.update)
        else:
            pass
    def select_file(self):
        reply = QMessageBox.question(self, '提示', '请选择bin文件之后进行操作,以免不必要的异常', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.load_file()
        else:
            pass

    def show_confirm_message(self):
        reply = QMessageBox.question(self, '提示', "是否重置", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reset_data()
        else:
            pass
    def send(self):
        """
        pushbutton_send控件点击触发的槽
        :return:
        """
        # 连接时根据用户选择的功能调用函数
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 1:
            self.tcp_send()
        if self.comboBox_tcp.currentIndex() == 2 or self.comboBox_tcp.currentIndex() == 3:
            self.udp_send()
        if self.comboBox_tcp.currentIndex() == 4:
            self.web_send()

    def click_clear(self):
        """
        pushbutton_clear控件点击触发的槽
        :return: None
        """
        # 清空接收区屏幕
        self.textBrowser_recv.clear()

    def click_dir(self):
        # WEB服务端功能中选择路径
        self.web_get_dir()

    def close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        # 连接时根据用户选择的功能调用函数
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 1:
            self.tcp_close()
        if self.comboBox_tcp.currentIndex() == 2 or self.comboBox_tcp.currentIndex() == 3:
            self.udp_close()
        if self.comboBox_tcp.currentIndex() == 4:
            self.web_close()
        self.reset()

    def reset(self):
        """
        功能函数，将按钮重置为初始状态
        :return:None
        """
        self.link = False
        self.client_socket_list = list()
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def another_window(self):
        """
        开启一个新的窗口的方法
        :return:
        """
        # 弹出一个消息框，提示开启了一个新的窗口
        QtWidgets.QMessageBox.warning(self,
                                      'TCP/UDP云台助手',
                                      "已经禁止串口模式,有需要请与标哥联系",
                                      QtWidgets.QMessageBox.Yes)
        # # 计数，开启了几个窗口
        # self.num = self.num + 1
        # # 开启新的窗口
        # self.another = MainWindow(self.num)
        # self.another.show()
        # 在这里开启串口模式
        # nn = ui_person.show()
        # mm = ui.hide()

        # myshow = Pyqt5_Serial()
        # myshow.show()
        # myshow.exec()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow(1)
    ui.show()
    sys.exit(app.exec_())
