import serial
import serial.tools.list_ports
import threading
import Illustrate

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
    if port is None:
        port = port_case
    process_str = ""
    timestamp = 0
    data = 0
    while True:
        """ portCase.in_waiting is length of buffer data"""
        if port.in_waiting:
            receive_str = port.read(port.in_waiting).decode("utf-8")
            if "WD_EXIT" in receive_str:
                break
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
                    continue
                if not (pos_first_t < pos_first_s < pos_first_d < pos_first_e):
                    continue
                timestamp = process_str[pos_first_t + 1:pos_first_s]
                data = process_str[pos_first_d + 1:pos_first_e]
                timestamp = int(timestamp)
                data = int(data)
                pass  # todo: add illustrating function
                print("timestamp:", timestamp)
                print("data:", data)
                print()
                process_str = ""


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


if __name__ == '__main__':
    # showAvailablePort()
    if openPort(port="COM3") == -1:
        print("Open port failed")
        exit()
    sendData("Serial Receiver Ready\r\n")
    port_read_thread = PortReadThread()
    port_read_thread.start()
    port_read_thread.join()
    Illustrate.showWindow()
    port_case.close()
    print("Port Closed")
