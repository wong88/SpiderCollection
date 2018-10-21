import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginBilibili(object):
    """Biblibili"""

    def __init__(self, username, password):
        # 起始登陆url
        self.url = 'https://passport.bilibili.com/login'
        # 生成webdriver对象
        self.browser = webdriver.Chrome()
        # 生成一个有等待的对象
        self.wait = WebDriverWait(self.browser, 20)
        # 用户名
        self.username = username
        #　密码
        self.password = password

    def __del__(self):
        """设置结束后关闭"""

        time.sleep(15)
        self.browser.close()

    def open(self):
        """打开网页,输入用户名和密码"""

        # 通过browser对象发送请求
        self.browser.get(self.url)
        # 将用户名和密码设置进等待的对象
        username = self.wait.until(EC.presence_of_element_located((By.ID, "login-username")))
        password = self.wait.until(EC.presence_of_element_located((By.ID, "login-passwd")))
        # 输入用户名密码
        username.send_keys(self.username)
        password.send_keys(self.password)

    def show_img(self):
        """鼠标悬停,显示极验图片"""

        # 获取悬停对象
        div_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gt_slider")))
        # 开始悬停
        ActionChains(self.browser).move_to_element(div_element).perform()

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        # 屏幕截图
        screenshot = self.browser.get_screenshot_as_png()
        # 获取截图对象
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_position(self):
        """获取图片所在标签的位置信息
        Returns:返回截图区域信息
        """
        # 通过xpath获取img对象
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='gt_cut_fullbg gt_show']")))
        time.sleep(2)
        location = img.location
        # 获取图片尺寸
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_image(self, name='captcha.png'):
        """根据位置信息,通过截图获取验证码图片
        :return: 图片对象
        """
        # 获取四边范围
        top, bottom, left, right = self.get_position()
        # 获取截图对象
        screenshot = self.get_screenshot()
        # 截图
        captcha = screenshot.crop((left, top, right, bottom))
        #保存图片
        captcha.save(name)
        return captcha

    def get_slider(self):
        """获取滑块
        :return: 滑块对象
        """

        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='gt_slider_knob gt_show']")))
        return slider

    def get_gap(self, image1, image2):
        """通过对比像素点,获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return: 偏移量的大小
        """
        left = 65
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 58
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                        pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """根据偏移量获取移动的轨迹列表
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹, 即每次移动的距离,为一个列表,总和等于偏移量
        track = []
        # 当前位移, 也即记录当前移动了多少距离
        current = 0
        # num = random.randint(1,5)
        # 减速阈值, 也即开始减速的位置,这里设置为偏移量的4/5处开始减速,可以更改
        mid = distance * 2 / 5
        # 计算用的时间间隔
        t = 0.3
        # 初始速度
        v = 0

        while current < distance:
            if current < mid:
                # 当前位移小于2/5的偏移量时,加速度为2
                a = 2
            else:
                # 当前位移大于2/5的偏移量时,加速度为-3
                a = -3
            # 初始速度v0
            v0 = v
            # 本次移动完成之后的速度v = v0 + at
            v = v0 + a * t
            # 本次移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移, 这里都将move四舍五入取整
            current += round(move)
            # 将move的距离放入轨迹列表
            track.append(round(move))

        return track

    def move_slider(self, slider, track):
        """根据轨迹列表,拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        """
        # 设置为滑动
        ActionChains(self.browser).click_and_hold(slider).perform()
        # 通过遍历轨迹列表的运动轨迹运动
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        # 开始运动
        ActionChains(self.browser).release().perform()

    def run_spider(self):
        # 打开网页,传入用户名和密码
        self.open()
        while True:
            # 鼠标悬停,显示图片
            self.show_img()
            # 获取无缺口验证码截图,保存
            img_1 = self.get_image(name='data/img1.png')
            # 获取滑块对象
            slider = self.get_slider()
            # 点击滑块对象,显示有缺口的验证码图片
            slider.click()
            # 等待1.5秒, 让点击之后出现提示消失, 方便截图
            time.sleep(1.5)
            # 获取有缺口的验证码截图,保存
            img_2 = self.get_image(name='data/img2.png')
            # 获取偏移量大小
            gap = self.get_gap(img_1, img_2)

            # 根据偏移量的值, 计算移动轨迹, 得到轨迹列表
            track = self.get_track(gap - 6)

            # 根据轨迹列表, 移动滑块
            self.move_slider(slider, track)
            time.sleep(2)
            cookies = self.browser.get_cookies()
            if len(cookies) > 5:
                print(cookies)
                break
            time.sleep(3)


def main():
    username = '********'
    password = '********'
    crack_bilibili = LoginBilibili(username, password)
    crack_bilibili.run_spider()


if __name__ == '__main__':
    main()