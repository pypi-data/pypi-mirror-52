from DiaLogger import Logger
import win32gui, win32con,win32ui
from time import sleep
from PIL import Image
import os,threading
import aircv as ac
import os ,cv2,datetime

from skimage import io
log = Logger()
path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(path))

class Picture:
    def __init__(self,hwnd):
        self._hwnd = hwnd
        self._pic = None
        self.lock = threading.Lock()
    def CheckWindowHandle(self):
        if self._hwnd == 0:
            log.logger.warning("window handle not found  ! errCode : 10001")
            return None
        else:
            return 1
    def MatchThePicture(self,matchedPicture,confidence = 0.6):
        if self._pic == None:
            log.logger.warning("current picture not found  ! errCode : 11001")
            return None
        if matchedPicture == None:
            log.logger.warning("matched picture not found  ! errCode : 11002")
            return None
        imsrc = ac.imread(self._pic)
        imobj = ac.imread(matchedPicture)
        match_result = ac.find_template(imsrc, imobj, confidence)
        # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
        if match_result is not None:
            match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
            match_result['result'] = (int(match_result['result'][0]), int(match_result['result'][1]))
        return match_result

    def MatchThePictureRegion(self,matchedPicture,region,confidence = 0.6):
        self.CaptureTheCurrentScreen()
        sleep(0.2)
        log.logger.warning("区域截图")
        img = Image.open(self._pic)
        re = img.crop(region)
        re.save(os.path.join("../resource\\Capture", 'CurrentScreen_region.png'))
        imsrc = ac.imread(os.path.join("../resource\\Capture", 'CurrentScreen_region.png'))
        imobj = ac.imread(matchedPicture)
        match_result = ac.find_template(imsrc, imobj, confidence)
        if match_result is not None:
            match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
            match_result['result'] = (int(match_result['result'][0]), int(match_result['result'][1]))
        return match_result

    def MatchTheTaskPage(self,task):
        self.CaptureTheCurrentScreen()
        sleep(0.2)
        for k, v in task.items():
            pagePic = v.get("pic")
            pagePicUrl = os.path.join("../resource", "Page", str(pagePic))
            rate = self.MatchThePicture(pagePicUrl,float(v.get("confidence")))
            if rate != None:
                log.logger.info("currentPage  : " + str(k))
                return k
        return None
    def GetCurrentPoint(self,point):
        self.CaptureTheCurrentScreen()
        sleep(0.25)
        # img = io.imread(self._pic)
        # result = img[point[1]][point[0]]
        img = Image.open(self._pic)
        img_array = img.load()
        result = img_array[point[0],point[1]][1]
        log.logger.info("skimage  result : " + str(result))
        return result

    def GetCurrentPointRGB(self,point):
        self.CaptureTheCurrentScreen()
        sleep(0.25)
        # img = io.imread(self._pic)
        # result = img[point[1]][point[0]]
        img = Image.open(self._pic)
        img_array = img.load()
        result = img_array[point[0],point[1]]
        log.logger.info("skimage  result : " + str(result))
        return result

    def CaptureTheCurrentScreen(self):  # 获取当前窗口DCF图片
        self.lock.acquire()
        if self.CheckWindowHandle() == 1:
            # 增加延时
            sleep(0.1)
            left, top, right, bot = win32gui.GetWindowRect(self._hwnd)
            SW = right - left
            SH = bot - top
            # print(SW)
            # print(SH)
            # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
            wDC = win32gui.GetWindowDC(self._hwnd)
            # 创建设备描述表
            dcObj = win32ui.CreateDCFromHandle(wDC)
            # 创建内存设备描述表
            saveDC = dcObj.CreateCompatibleDC()
            # 创建位图对象
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(dcObj, SW, SH)
            saveDC.SelectObject(saveBitMap)
            # 截图至内存设备描述表
            img_dc = dcObj
            mem_dc = saveDC
            mem_dc.BitBlt((0, 0), (SW, SH), img_dc, (0, 0), win32con.SRCCOPY)
            # 将截图保存到文件中
            # saveBitMap.SaveBitmapFile(mem_dc, 'C:\\Users\\Dia\\Desktop\\current.png')
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            # 生成图像
            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
            # 内存释放
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            dcObj.DeleteDC()
            win32gui.ReleaseDC(self._hwnd, wDC)
            #im.save(os.path.join(BASE_DIR + "\\resource\\Capture", 'CurrentScreen.png'))
            #self._pic = os.path.join(BASE_DIR + "\\resource\\Capture", 'CurrentScreen.png')
            im.save("../resource\\Capture\\CurrentScreen.png")
            self._pic = "../resource\\Capture\\CurrentScreen.png"
            log.logger.info('Capture the current screen...')
        self.lock.release()