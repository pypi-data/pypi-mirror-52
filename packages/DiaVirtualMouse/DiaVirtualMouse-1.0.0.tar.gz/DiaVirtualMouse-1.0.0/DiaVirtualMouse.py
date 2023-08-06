from DiaLogger import Logger
from time import sleep, time
import win32api, win32con
import os, random,threading

log = Logger()
path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(path))


class Mouse:
    def __init__(self, hwnd):
        self._hwnd = hwnd
        self.point = None
        self.lock = threading.Lock()
    def CheckWindowHandle(self):
        if self._hwnd == 0:
            log.logger.warning("window handle not found  ! errCode : 10001")
            return None
        else:
            return 1

    def LeftClick(self, point):
        if self.CheckWindowHandle != 0:
            x = point[0] + random.randint(-10, 10)
            y = point[1] + random.randint(-10, 10)
            long_position = win32api.MAKELONG(x, y)
            long_position2 = win32api.MAKELONG(x + random.randint(-100, 100),
                                               y + random.randint(-200, 200))
            long_position3 = win32api.MAKELONG(x + random.randint(-220, 220),
                                               y + random.randint(-230, 240))
            win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position2)
            sleep(random.uniform(0.01, 0.08))
            win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position3)
            sleep(random.uniform(0.01, 0.08))
            win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position)
            sleep(0.1)
            win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position)
            sleep(0.1)
            win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
            sleep(random.uniform(0.06, 0.13))
            win32api.PostMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
            log.logger.info('Mouse.LeftClick point ' + '(' + str(x) + ", " + str(y) + ')')

        else:
            log.logger.warning('errCode null')

    def LeftClick2(self, point):
        if self.CheckWindowHandle != 0:
            x = point[0] + random.randint(-5, 5)
            y = point[1] + random.randint(-5, 5)
            long_position = win32api.MAKELONG(x, y)
            win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
            sleep(random.uniform(0.06, 0.13))
            win32api.PostMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
            log.logger.info('Mouse.LeftClick point ' + '(' + str(x) + ", " + str(y) + ')')
        else:
            log.logger.warning('errCode null')

    def LeftClick3(self, point):
        if self.CheckWindowHandle != 0:
            x = point[0] + random.randint(-3, 5)
            y = point[1] + random.randint(-3, 5)
            long_position = win32api.MAKELONG(x, y)

            win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
            sleep(random.uniform(0.06, 0.13))
            win32api.PostMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
            log.logger.info('Mouse.LeftClick point ' + '(' + str(x) + ", " + str(y) + ')')
        else:
            log.logger.warning('errCode null')

    def LeftClick4(self, point):
        if self.CheckWindowHandle != 0:
            x = point[0] + random.randint(-3, 5)
            y = point[1] + random.randint(-1, 2)
            long_position = win32api.MAKELONG(x, y)

            win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
            sleep(random.uniform(0.06, 0.13))
            win32api.PostMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
            log.logger.info('Mouse.LeftClick point ' + '(' + str(x) + ", " + str(y) + ')')
        else:
            log.logger.warning('errCode null')

    def KeyboardClick(self, args):
        sleep(0.1)
        for arg in args:
            win32api.SendMessage(self._hwnd, win32con.WM_KEYDOWN, arg, 0)
            log.logger.info('Mouse.KeyboardClick  ' + '(' + str(arg) + ')')
        for arg in args:
            win32api.SendMessage(self._hwnd, win32con.WM_KEYUP, arg, 0)

    def MouseHover(self,point):
        x2 = point[0] + random.randint(-5, 5)
        y2 = point[1] + random.randint(-5, 5)
        long_position2 = win32api.MAKELONG(x2, y2)
        win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position2)

    def LeftMouseMove(self,beginPoint,endPoint):
        self.lock.locked()
        x = beginPoint[0] + random.randint(-5, 5)
        y = beginPoint[1] + random.randint(-5, 5)
        long_position = win32api.MAKELONG(x, y)

        x2 = endPoint[0] + random.randint(-5, 5)
        y2 = endPoint[1] + random.randint(-5, 5)
        long_position2 = win32api.MAKELONG(x2, y2)

        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        sleep(random.uniform(0.05, 0.1))
        win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position2)
        sleep(random.uniform(0.4, 0.6))
        win32api.PostMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position2)
        self.lock.locked()
        log.logger.info('Mouse.LeftMouseMove point ' + '(' + str(x) + ", " + str(y) + ')  to ' + '(' + str(x2) + ", " + str(y2) + ')')

    def LeftMouseMove2(self,beginPoint,endPoint):
        self.lock.locked()
        x = beginPoint[0]
        y = beginPoint[1]
        long_position = win32api.MAKELONG(x, y)
        x2 = endPoint[0]
        y2 = endPoint[1]
        long_position2 = win32api.MAKELONG(x2, y2)

        # 一个窗口被激活或失去激活状态
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.WM_ACTIVATE, long_position)
        # 杀死焦点
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.WM_KILLFOCUS, long_position)

        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        sleep(random.uniform(0.1, 0.2))
        win32api.SendMessage(self._hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position2)
        sleep(random.uniform(1, 5))
        win32api.PostMessage(self._hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position2)
        self.lock.locked()
        log.logger.info('Mouse.LeftMouseMove point ' + '(' + str(x) + ", " + str(y) + ')  to ' + '(' + str(x2) + ", " + str(y2) + ')')

# def main():
#     # 根据类名及标题名查询句柄，
#     hwnd = win32gui.FindWindow("Win32Window0", "阴阳师-网易游戏")
#     # 查找指定句柄的子句柄，后两个参数为子类的类名与标题，如果没有或不确定，可以写None
#     # hwnd = win32gui.FindWindow(hwnd, None, "sub_class", "sub_title")
#     print('获取窗口')
#     print(hwnd)
#     sleep(0.1)
#
#     # 没有直接修改窗口大小的方式，但可以曲线救国，
#     # 几个参数分别表示句柄,起始点坐标,宽高度,是否重绘界面 ，如果想改变窗口大小，就必须指定起始点的坐标，没果对起始点坐标没有要求，随便写就可以；如果还想要放在原先的位置，就需要先获取之前的边框位置，再调用该方法即可
#     win32gui.MoveWindow(hwnd, 20, 20, 800, 600, False)
#     print('调整窗口大小')
#
#     # 指定句柄设置为前台，也就是激活
#     # win32gui.SetForegroundWindow(hwnd)
#     # 设置为后台
#     win32gui.SetBkMode(hwnd, win32con.TRANSPARENT)
#     print('设置为后台')
#
#     # 在这里两几种方式可以选择 可以使用win32gui包和win32api的包，目前未深入了解，感觉是一样的，每一个里面还有PostMessage与SendMessage两都可选，依据其他文档的说法是SendMessage是同步的，在成功执行后才会返回，而PostMessage是异步执行的，直接返回，只是把内容加在队列里
#     # 几个参数分别为: 操作的句柄 , 按键的类型(是按下或者是弹起), 键码（大部分的功能键在win32con包中都，对于常用的数字或字母，直接去查找ASII码即可，如A 65 等等），相对于句柄中的位置(在这里需要使用win32api.MAKELONG(x,y)将两个地址转换为一个长地址；
#     # 在这种情况下，可以做到后台的操作
#     # 需要注意的是每一个按键要有按下与弹起两个过程，比果我们要按Enter键，就需要有两句代码，第二个参数分别为 KEYDOAWN与 KEYUP ，如果是组合键，就先把组合键分别按下后再分别弹起即可
#     # win32gui.PostMessage(tid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
#     # win32gui.SendMessage(tid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
#     print('开始点击')
#     long_position = win32api.MAKELONG(30, 30)
#     sleep(0.1)
#     win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
#     sleep(0.1)
#     win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
#
# main()
