#! /usr/bin/env python3.7.4
# -*- coding:utf-8 -*-
# @Author : Linwenyuan
# @Software: PyCharm
# @Date: 2021/08/17
# @github:https://blog.csdn.net/yanchuandong/article/details/109484409#comments_17393942

import xlrd         #处理excel的库
import time
import datetime
import paramiko     #处理ssh的库
import telnetlib    #处理ssh的库
from timer import Timer

now = datetime.datetime.now()


class Switchbak():

    def __init__(self,excel,sheet1,sheet2,save_path):
        self.excel = excel
        self.sheet1 = sheet1
        self.sheet2 = sheet2
        self.save_path = save_path


    def bak(self):

        #print('执行到switchbak里头啦')
        # 按工作表名称选择sheet1（交换机信息）和sheet2（命令）的工作表
        workbook = xlrd.open_workbook(self.excel)
        opened_sheet1 = workbook.sheet_by_name(self.sheet1)
        opened_sheet2 = workbook.sheet_by_name(self.sheet2)
        # 把需要敲打的命令提取到info_cmd数组里头
        info_cmd = opened_sheet2.col_values(0)
        #print (str(now.strftime('%Y-%m-%d %H:%M:%S ')) + type(info_cmd))

        for a in range(1, opened_sheet1.nrows):
            #print('循环第'+ str(a) +'遍')
            # 将一行数据传给info数组
            info_sw = opened_sheet1.row_values(a)
            # 按数组下标赋值给对应变量
            host = str(info_sw[0])
            ip = str(info_sw[1])
            username = str(info_sw[2])
            password = str(info_sw[3])
            xieyi = str(info_sw[4])
            #print(host+' '+ip+' '+username+' '+password+' '+xieyi)

            if xieyi == 'SSH2':
                #ssh2_bak()
                try:
                    # 建立ssh连接
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=ip, username=username, password=password)
                    #print(str(now.strftime('%Y-%m-%d %H:%M:%S ')) + '正在备份 ' + str(host) + ' ' + str(ip))
                    print(str(Timer.shijian()) +  '正在备份 ' + str(host) + ' ' + str(ip))

                    # 调用shell
                    command = ssh.invoke_shell()

                    #ssh2_bak实例化，然后再输出
                    #ssh2_bak(info_cmd,host,username,password)
                    for b in range(1, opened_sheet2.nrows):
                        #print('opened_sheet2.nrows='+str(opened_sheet2.nrows)+'  b ='+str(b))
                        output = (command.send(str(info_cmd[b]) + "\n"))
                        # 程序暂停3秒
                        #print(str(now.strftime('%Y-%m-%d %H:%M:%S ')) + '正在执行 ' + str(info_cmd[b]))
                        print(str(Timer.shijian()) +  '正在执行 ' + str(info_cmd[b]))
                        time.sleep(3)

                    # 输出交换机配置到文件
                    output = command.recv(655355).decode("utf8","ignore")
                    file = open('%s/%s' % (self.save_path, host + '.txt'), 'a+')
                    file.write(output)

                    # 结束
                    file.close()
                    ssh.close()

                    # 输出日志
                    print(str(Timer.shijian()) +  host + ' 备份完成')
                    print(' ')
                    print('*********************************************************')
                    print(' ')

                except:
                    #输出失败日志
                    print(str(Timer.shijian()) +  host + ' 备份失败！！！！！')
                    print(' ')
                    print('*********************************************************')
                    print(' ')


            elif xieyi == 'TELNET':
                #telnet_bak(info_cmd)
                try:
                    #建立telnet连接
                    tn = telnetlib.Telnet(ip,port=23,timeout=15)
                    #tn.set_debuglevel(5)

                    #输入用户名密码
                    time.sleep(3)
                    #tn.read_until('Username:')
                    #c = tn.read_all()
                    #print(str(c))
                    tn.write(username.encode('ascii') +b'\n')
                    #print('输入用户名成功')
                    time.sleep(1)
                    #tn.read_until('Password:')
                    tn.write(password.encode('ascii') +b'\n')
                    #print('输入密码成功')
                    time.sleep(1)

                    #执行命令
                    for b in range(1, opened_sheet2.nrows):
                        #print('opened_sheet2.nrows='+str(opened_sheet2.nrows)+'  b ='+str(b))
                        tn.write((str(info_cmd[b]) + "\n").encode('ascii'))
                        # 程序暂停3秒
                        print(str(Timer.shijian()) +  '正在执行 ' + str(info_cmd[b]))
                        time.sleep(3)

                    #获取输出内容到文件,如果用read_all()的话，如果回显没返回EOF也会卡在这里。比较好的做法是使用read_very_eager()，最多加个延迟就可拿到全部的结果。
                    #decode("utf8","ignore") 不加的话会执行不下去
                    output = tn.read_very_eager().decode("utf8","ignore")
                    file = open('%s/%s' % (self.save_path, host + '.txt'), 'a+')
                    file.write(output)

                    #结束
                    file.close()
                    tn.close()

                    # 输出日志
                    print(str(Timer.shijian()) +  host + ' 备份完成')
                    print(' ')
                    print('*********************************************************')
                    print(' ')

                except:
                    # 输出失败日志
                    print(str(Timer.shijian()) +  host + ' 备份失败！！！！！')
                    print(' ')
                    print('*********************************************************')
                    print(' ')

            else:
                print(str(Timer.shijian()) + host +' '+ ip + "采集失败，请确认登录协议是否为'SSH2''或者'TELNET'")
                print(' ')
                print('*********************************************************')


