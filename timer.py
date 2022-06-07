# -*- coding:utf-8 -*-
# @Date: 2021/08/13
# @Author : xiaomumu

import time


class Timer():

    def shijian():
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "  --  "


