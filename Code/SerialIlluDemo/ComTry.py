import serial
import serial.tools.list_ports
import threading
import pyqtgraph as pg
import array
from PyQt5.QtCore import QTimer
import numpy as np

using_port = "COM4"
using_baud_rate = 115200
using_timeout = 1
port_case = serial.Serial()


class PortReadThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("PortReadThread started")
        getData(self.name)
        print("PortReadThread halted")


def getData(thread_name, port=None):
    pass


#     if port is None:
#         port = port_case
#     process_str = ""
#     timestamp = 0
#     data = 0
#     while True:
#         """ portCase.in_waiting is length of buffer data"""
#         if port.in_waiting:
#             receive_str = port.read(port.in_waiting).decode("utf-8")
#             if "WD_EXIT" in receive_str:
#                 break
#             else:
#                 """ Input format: T(timestamp)S D(data)E"""
#                 # TODO: improve robustness (Read buffer)
#                 process_str += receive_str
#                 pos_first_t = -1
#                 pos_first_s = -1
#                 pos_first_d = -1
#                 pos_first_e = -1
#                 for i in range(len(process_str)):
#                     if process_str[i] == 'T' and pos_first_t == -1:
#                         pos_first_t = i
#                     if process_str[i] == 'S' and pos_first_s == -1:
#                         pos_first_s = i
#                     if process_str[i] == 'D' and pos_first_d == -1:
#                         pos_first_d = i
#                     if process_str[i] == 'E' and pos_first_e == -1:
#                         pos_first_e = i
#                 if pos_first_s == -1 or pos_first_t == -1 or pos_first_d == -1 or pos_first_e == -1:
#                     continue
#                 if not (pos_first_t < pos_first_s < pos_first_d < pos_first_e):
#                     continue
#                 timestamp = process_str[pos_first_t + 1:pos_first_s]
#                 data = process_str[pos_first_d + 1:pos_first_e]
#                 timestamp = int(timestamp)
#                 data = int(data)
#                 pass  # todo: add illustrating function
#                 print("timestamp:", timestamp)
#                 print("data:", data)
#                 print()
#                 process_str = ""


def openPort(port="", bdr=0, timeout=0):
    """
    这个函数定义了串口的打开操作，它会返回一个打开的串口示例
    输入说明：port为串口号，bdr为波特率。如果为空则使用默认设置
    """
    global port_case
    if port == "":
        port = using_port
    if bdr == 0:
        bdr = using_baud_rate
    if timeout == 0:
        timeout = using_timeout
    try:
        port_case = serial.Serial(port, bdr, timeout=timeout)
    except Exception as error:
        print("Open Port Failed: ", error)
        return -1
    return port_case


def showAvailablePort():
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
    else:
        for i in range(0, len(port_list)):
            print(port_list[i])


def sendData(data, port=None):
    """ Note: Default parameter must be const value"""
    """
    发送数据，传入的data必须是一个字符串
    port为端口实例，默认值是portCase（全局默认实例）
    """
    if port is None:
        port = port_case
    port.write(data.encode("utf-8"))


curve_data = []
current = -1
last_pos = -1


def tryGetData(port=None):
    if port is None:
        port = port_case
    process_str = ""
    timestamp = 0
    data = 0
    """ portCase.in_waiting is length of buffer data"""
    if port.in_waiting:
        receive_str = port.read(port.in_waiting).decode("utf-8")
        print(receive_str)
        if "WD_EXIT" in receive_str:
            return  # todo: such will not work properly
        else:
            """ Input format: T(timestamp)S D(data)E"""
            # TODO: improve robustness (Read buffer)
            process_str += receive_str
            pos_first_t = -1
            pos_first_s = -1
            pos_first_d = -1
            pos_first_e = -1
            for i in range(len(process_str)):
                if process_str[i] == 'T' and pos_first_t == -1:
                    pos_first_t = i
                if process_str[i] == 'S' and pos_first_s == -1:
                    pos_first_s = i
                if process_str[i] == 'D' and pos_first_d == -1:
                    pos_first_d = i
                if process_str[i] == 'E' and pos_first_e == -1:
                    pos_first_e = i
            if pos_first_s == -1 or pos_first_t == -1 or pos_first_d == -1 or pos_first_e == -1:
                return
            if not (pos_first_t < pos_first_s < pos_first_d < pos_first_e):
                return
            timestamp = process_str[pos_first_t + 1:pos_first_s]
            data = process_str[pos_first_d + 1:pos_first_e]
            timestamp = int(timestamp)
            data = int(data)
            global current
            if current == -1:
                current = timestamp
                curve_data.append(data)
            else:
                # todo: can be rewrite by numpy
                while current < timestamp:
                    curve_data.append(curve_data[-1]+(data - curve_data[-1])/(timestamp-current))
                    current += 1
            curve.setData(curve_data)

            print("timestamp:", timestamp)
            print("data:", data)
            print()
            process_str = ""


app = pg.mkQApp()  # 建立app
# todo: use object "GraphicsLayoutWidget" to replace deprecated "GraphicsWindow"
win = pg.GraphicsWindow()  # 建立窗口
win.setWindowTitle("sin demo")
win.resize(800, 500)  # 小窗口大小
data = array.array('d')  # 可动态改变数组的大小,double型数组
historyLength = 70000  # 横坐标长度
p = win.addPlot()  # 把图p加入到窗口中
p.showGrid(x=True, y=True)  # 把X和Y的表格打开
p.setRange(xRange=[0, historyLength], yRange=[-120, 120], padding=0)
p.setLabel(axis='left', text='y / V')  # 靠左
p.setLabel(axis='bottom', text='x / point')
p.setTitle('y = chart')  # 表格的名字
curve = p.plot()  # 绘制一个图形
idx = 0

if __name__ == '__main__':
    # showAvailablePort()
    if openPort(port="COM13") == -1:
        print("Open port failed")
        exit()
    sendData("Serial Receiver Ready\r\n")
    timer = QTimer()
    timer.timeout.connect(tryGetData)
    timer.start(0)  # Change the illustrate data
    app.exec_()
    port_case.close()
    print("Port Closed")
