import serial
import serial.tools.list_ports
import threading
import pyqtgraph as pg
import array
from line_profiler import LineProfiler
from PyQt5.QtCore import QTimer
import numpy as np
import time

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


def countTime():
    profile = LineProfiler(tryGetData)
    profile.runcall(tryGetData)
    profile.print_stats()


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


curve_data = np.zeros(1, dtype=int)
last_timestamp = -1
last_data = -1
current = -1
last_pos = -1

locked = 0

process_str = ""


def tryGetData(port=None):
    print("new")
    global process_str
    if port is None:
        port = port_case
    pos_first_t = -1
    pos_first_s = -1
    pos_first_d = -1
    pos_first_e = -1
    try:
        process_str += port.read(port.in_waiting).decode("utf-8")
    except Exception as error:
        print(error)
        return
    while True:
        """ portCase.in_waiting is length of buffer data"""
        if port.in_waiting and pos_first_t != -1:
            try:
                process_str += port.read(port.in_waiting).decode("utf-8")
            except Exception as error:
                print(error)
                continue
        if len(process_str) > 10000:  # Buffer size
            process_str = process_str[len(process_str) // 2:]
        """ Input format: T(timestamp)S D(data)E"""
        if pos_first_t == -1:
            pos_first_t = process_str.find('T')
        if pos_first_t != -1 and pos_first_s == -1:
            pos_first_s = process_str.find('S', pos_first_t)
        if pos_first_s != -1 and pos_first_d == -1:
            pos_first_d = process_str.find('D', pos_first_s)
        if pos_first_d != -1 and pos_first_e == -1:
            pos_first_e = process_str.find('E', pos_first_d)
        if pos_first_t == -1:
            return
        if pos_first_e == -1:
            return
        timestamp = process_str[pos_first_t + 1:pos_first_s]
        data = process_str[pos_first_d + 1:pos_first_e]
        timestamp = int(timestamp)
        data = int(data)
        global last_timestamp
        global last_data
        global curve_data
        if last_timestamp == -1:
            last_timestamp = timestamp
            last_data = data
            curve_data[0] = data
        else:
            if timestamp < last_timestamp:
                current_data = np.zeros(5000)
            elif timestamp == last_timestamp:
                process_str = process_str[pos_first_e + 1:]
                pos_first_t = -1
                pos_first_s = -1
                pos_first_d = -1
                pos_first_e = -1
                continue
            else:
                current_data = np.linspace(last_data, data, timestamp - last_timestamp + 1)
            current_data = current_data[1:]
            last_timestamp = timestamp
            last_data = data
            curve_data = np.concatenate((curve_data, current_data))
            process_str = process_str[pos_first_e + 1:]
            pos_first_t = -1
            pos_first_s = -1
            pos_first_d = -1
            pos_first_e = -1


def draw():
    curve.setData(curve_data)


app = pg.mkQApp()  # 建立app
# todo: use object "GraphicsLayoutWidget" to replace deprecated "GraphicsWindow"
win = pg.GraphicsWindow()  # 建立窗口
win.setWindowTitle("sin demo")
win.resize(800, 500)  # 小窗口大小
data = array.array('d')  # 可动态改变数组的大小,double型数组
historyLength = 10000  # 横坐标长度
p = win.addPlot()  # 把图p加入到窗口中
p.showGrid(x=True, y=True)  # 把X和Y的表格打开
p.setRange(xRange=[0, historyLength], yRange=[-120, 120], padding=0)
p.setLabel(axis='left', text='y / V')  # 靠左
p.setLabel(axis='bottom', text='x / ms')
curve = p.plot()  # 绘制一个图形

if __name__ == '__main__':
    # showAvailablePort()
    if openPort() == -1:
        print("Open port failed")
        exit()
    sendData("Serial Receiver Ready\r\n")
    timer1 = QTimer()
    timer1.timeout.connect(tryGetData)
    timer1.start(6)  # Change the illustrate data
    timer2 = QTimer()
    timer2.timeout.connect(draw)
    timer2.start(6)  # GetData
    app.exec_()
    port_case.close()
    print("Port Closed")
