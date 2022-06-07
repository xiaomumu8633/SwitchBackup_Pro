#! /usr/bin/env python3.7.4
# -*- coding:utf-8 -*-
# @Author : Linwenyuan
# @Software: PyCharm
# @Date: 2021/08/17
# @github:https://github.com/xiaomumu8633/SwitchBackup_Pro


import os
import datetime
import xlrd

from switchbak import Switchbak
from timer import Timer

if __name__ == '__main__':
    a = """
    本程序用于交换机自动备份，请管理员保管好交换机用户密码，勿将本程序用于任何商业用途！
    在程序运行之前，请确认配置文件“Network Equipment Info.xlsx”是否和“main.exe”在同一个文件夹下。 
    
    有问题请访问Github:    https://github.com/xiaomumu8633/SwitchBackup_Pro
                                                                                
                                                        --------xiaomumu8633  """
    print(a)
    input("请按任意键开始运行：" )

    # 获取当前时间
    now = datetime.datetime.now()
    #print(now)
    # 设置输出路径及时间戳格式
    path = "./bak/%s" % now.strftime('%Y%m%d')
    #print('path = '+ path)

    # 看配置文件是否存在
    if not os.path.isfile('Network Equipment Info.xlsx'):
        input(str(Timer.shijian())  +"在主目录下没有找到'Network Equipment Info.xlsx',程序无法执行，请输入任意键继续。")

    # 创建存储目录
    if not os.path.exists(path):
        os.makedirs(path)


    # 打开Network Equipment Info.xlsx
    workbook = xlrd.open_workbook('Network Equipment Info.xlsx')
    # 按工作表名称选择Huawei工作表
    sheet = workbook.sheet_by_name('Config')
    #提取文件存储地址
    address=sheet.cell(0,1)
    #print(str(Timer.shijian()) + ' ' +'备份文件存储路径为： '+str(address))

    # 排除前两行后，遍历所有行的数据
    for a in range(2, sheet.nrows):
        #print('nrows = ' + str(sheet.nrows))
        #print(a)
        info = sheet.row_values(a)
        maker = str(info[0])
        #print(maker)
        maker_cmd = str(info[1])
        #print(maker_cmd)
        #print('path = ' + path)

        #开始运行备份命令
        switchbak = Switchbak('Network Equipment Info.xlsx',maker,maker_cmd,path)
        switchbak.bak()


input("交换机备份完成，请输入任意键退出!")
