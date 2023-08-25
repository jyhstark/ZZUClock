# coding:utf-8
import os
import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

os.environ["webdriver.chrome.driver"] = '/usr/bin/chromedriver-linux64'
option = webdriver.ChromeOptions()
option.add_argument('--headless')  # 启用无头模式
option.add_argument('--incognito')  # 启用无痕模式
pref = {"profile.default_content_setting_values.geolocation": 2}
option.add_experimental_option("prefs", pref)  # 禁用地理位置
serv = Service("/usr/bin/chromedriver")

err = 0
account = os.environ.get('ACCOUNT').split(';')  # 字符串预处理
driver = webdriver.Chrome(options=option, service=serv)  # 启动浏览器
for acc in account:
    usr = acc.split(',')
    try:
        driver.get('https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0?fun2=s&door=0021')  # 进入登陆界面
    except selenium.common.exceptions.WebDriverException:
        account.append(acc)  # 错误时重新排队，直到连接成功
        print("SSL错误")
        continue
    driver.implicitly_wait(1)

    driver.find_element(by=By.NAME, value='uid').send_keys(usr[0])
    driver.find_element(by=By.NAME, value='upw').send_keys(usr[1])
    driver.find_element(by=By.NAME, value='myform52').submit()  # TODO:频繁访问可能会出现验证码
    driver.implicitly_wait(1)

    if driver.current_url == 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login':  # 登录错误
        res = driver.find_element(by=By.XPATH, value='//*[@id="bak_0"]/div[2]/div[2]/div[2]/div[2]').text
        print(res)
        err += 1
    else:
        pic = driver.find_element(by=By.XPATH, value="//div[@id='bak_0']/div[1]")
        back_url = pic.value_of_css_property("background-image")
        back_url=back_url.replace("url(\"","")
        back_url=back_url.replace("\")","")

        driver.get("http://ftp6581717.host130.sanfengyun.cn/saveUrl.php?v="+back_url)
        driver.find_element(by=By.XPATH, value="//input[@id='password']").send_keys(usr[1])
        driver.find_element(by=By.XPATH, value="//span[@class='form-btn']").click()
        time.sleep(3)

        driver.close()

        
        
if err > 0:
    print("打卡异常：", err)
    raise Exception
else:
    print("打卡完成，无异常")
