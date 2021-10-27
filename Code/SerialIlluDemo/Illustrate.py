import array
import serial
import threading
import numpy as np
import time
import pyqtgraph as pg
from PyQt5.QtCore import QTimer



app = pg.mkQApp()

class WindowsThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # todo: use object "GraphicsLayoutWidget" to replace deprecated "GraphicsWindow"
        win = pg.GraphicsWindow()
        win.setWindowTitle('Dataset')
        win.resize(800, 500)

        data = array.array('d')
        horizon_length = 100
        pic = win.addPlot()
        pic.showGrid(x=True, y=True)
        pic.setRange(xRange=[0, horizon_length], yRange=[-1.2, 1.2], padding=0)
        pic.setLabel(axis='left', text='y / V')  # 靠左
        pic.setLabel(axis='bottom', text='x / point')
        pic.setTitle('Chart')  # 表格的名字
        curve = pic.plot()  # 绘制一个图形
        idx = 0

    def run(self):
        print("PortReadThread started")
        app.exec_()
        print("PortReadThread halted")


windows_thread = WindowsThread()
windows_thread.start()
windows_thread.join()

if __name__ == '__main__':
    pass
    # timer = QTimer()
    # timer.timeout.connect()
    # timer.start(50)  # Change the illustrate data
    # Open the graph window
