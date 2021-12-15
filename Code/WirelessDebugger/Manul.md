# Wireless Debugger

Lenor

## Description

This wireless debugger is a python upper-computer program, which can illustrate one continuous data stream.

The data  stream should be transmit by serial port in one way or another. To realize wireless communication, using a wireless serial port is recommended. The following test is using nRT24L01 module, operating under 0.5W(typical).

**Debugger can no longer be used for more than 2 hours continuously**

**At least one data must be sent every 10 min.**

## Usage

### Hardware connection

Connect the MCU's UART with upper-computer by wireless serial port module first.

Normally you should prepare two wireless serial port modules, and connect one to the MCU and another to the USB-to-TTL converter which is connect to the upper-computer. And each TX should be connected to corresponding RX.

### Configurate the upper-computer program

If first use:

To install required library, execute the following command in the program directory:

**Remember to bypass any proxy first!**

```Shell
pip install -r requirements.txt
```

Modify the "Main.py":

| Line | From   | To                       |
| ---- | ------ | ------------------------ |
| 9    | COM4   | According port number    |
| 10   | 115200 | According port baud rate |

### Configurate the MCU program

Whenever you want to send any data, you should send it in the following format with proper UART configured:

```latex
"T$timestamp$S$sep$D$data$E\r\n"
```

\$timestamp\$ can be anything that denote the current time (recommend in millisecond)

\$sep\$ can be any string that does not contain 'T'/'S'/'D'/'E', using '_' or nothing as separator is recommended.

\$data\$ can be any pure number, and must **be integer**, but scientific notation is strongly deprecated, and the number ought to be no longer than 10 digits.

Add "\\r\\n" in the end of those sending data will be very nice(don't know why...)

For instance, you can simply using this command to send the number 1(with "printf" redefined and using HAL library):

```C
printf("T%luS_D%dE\r\n",HAL_GetTick(), 1);
```

At least 1ms interval between each transmission is recommend.

**Warning: The UART must not be occupied all the time.**

### Using the program

After configuring the needed configuration, execute the "Main.py" , it should soon show a window, and as you send the first two data, the first curve should have been illustrated.

You can use mouse operation to drag/zoom the curve.

