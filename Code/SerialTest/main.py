import serial
import serial.tools.list_ports
import threading

usingPort = "COM12"
usingBaudRate = 115200
usingTimeOut = 1
portCase = serial.Serial()

# class PortReadThread(threading.Thread):


"""
这个函数定义了串口的打开操作，它会返回一个打开的串口示例
输入说明：port为串口号，bdr为波特率。如果为空则使用默认设置
"""


def openPort(port="", bdr=0, timeout=0):
    global portCase
    if port == "":
        port = usingPort
    if bdr == 0:
        bdr = usingBaudRate
    if timeout == 0:
        timeout = usingTimeOut
    portCase = serial.Serial(port, bdr, timeout=timeout)
    return portCase


def showAvailablePort():
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
    else:
        for i in range(0, len(port_list)):
            print(port_list[i])


"""
发送数据，传入的data必须是一个字符串
port为端口实例，默认值是portCase（全局默认实例）
"""


def sendData(data, port=portCase):
    port = portCase
    port.write(data.encode("utf-8"))


if __name__ == '__main__':
    showAvailablePort()
    openPort(port="COM8")
    sendData("asdfasdf")
