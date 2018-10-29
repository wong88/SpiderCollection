from selenium import webdriver
import time
# 输入用户名密码
username = input("请输入您的账号")
password = input("请输入您的密码")
# 选择Chrome浏览器
chrome = webdriver.Chrome()
# 访问百度贴吧首页
chrome.get('https://tieba.baidu.com/')
# 找到登陆按钮
chrome.find_element_by_xpath('//div[@class = "u_menu_item"]/a').click()
time.sleep(2)
# 选择账号密码登陆
chrome.find_element_by_id('TANGRAM__PSP_10__footerULoginBtn').click()
time.sleep(1)
# 输入账号密码
chrome.find_element_by_id('TANGRAM__PSP_10__userName').send_keys(username)
chrome.find_element_by_id('TANGRAM__PSP_10__password').send_keys(password)
time.sleep(3)
# 点击登陆
chrome.find_element_by_id('TANGRAM__PSP_10__submit').click()
time.sleep(3)
chrome.find_element_by_class_name('onekey_btn').click()
time.sleep(2)
# 点击一件签到按钮
chrome.find_element_by_xpath('//div [@class = "sign_detail_hd"]/a').click()
time.sleep(1)
# 点击一件签到
chrome.find_element_by_class_name('dialogJclose').click()
time.sleep(5)
chrome.quit()