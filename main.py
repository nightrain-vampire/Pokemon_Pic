# -*- coding:UTF-8 -*-
from cProfile import label
from cgitb import html
from bs4 import BeautifulSoup
import requests
import os
from langconv import Converter
import numpy as np


def Traditional2Simplified(sentence):
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


class downloader(object):

    def __init__(self):
        self.target = r'http://wiki.52poke.com/wiki/宝可梦列表%EF%BC%88按全国图鉴编号%EF%BC%89'  # 章节页
        self.root = 'http://wiki.52poke.com'        # Wiki根目录
        self.pockmon = []  # 存放神奇宝贝名和属性
        # self.names = []
        self.urls = []  # 存放神奇宝贝链接
        self.nums = 0  # 章节数
        self.divs = []  # 不同地区的table
        self.palces = ['关都', '城都', '丰缘', '神奧',
                       '合眾', '卡洛斯', '阿羅拉', '伽勒尔']  # 地区名
        # self.image = []  # 不同神奇宝贝的图片地址
        # self.down = []  # 图片地址及编号

    def first_process(self):
        r = requests.get(self.target)
        r.encoding = r.apparent_encoding
        html = r.text
        div_bf = BeautifulSoup(html, features='html.parser')

        for place in self.palces:
            name = 'roundy eplist s-' + place + ' sortable'
            print(name)
            self.divs.append(div_bf.find('table', class_=name))
        print(len(self.divs))

        for i in ['豐緣', '關都', '神奥', '合众', '阿罗拉']:
            self.palces.append(i)
        self.get_Pokemon()

    def get_Pokemon(self):
        for div in self.divs:
            l = []
            trs = div.find_all('tr')
            tmp = []
            tmp_url = []
            k = 0
            # 收集一个地区的所有信息
            for tr in trs:
                print('获取小精灵信息中…… {} %'.format(k*100/len(trs)), end='\r')
                k = k + 1
                # 解析每个宝可梦的名字，url
                lables = tr.find_all('a')
                if len(lables) > 2:
                    # 名称和 url 条目
                    label = lables[0]
                    tmp_url.append(self.root + label['href'])
                    name = label['title']       # 获取名字
                    attrs = []                   # 获取属性
                    for i in range(2, len(lables)):
                        attr = lables[i]['title']
                        attrs.append(attr)
                    tmp.append([name, attrs])
            # 以地区为单位更新
            self.pockmon.append(tmp)
            self.urls.append(tmp_url)
        # 打印宝可梦信息
        # root = './info'
        # for i in range(0, len(self.pockmon)):
        #     path = root + '/' + self.palces[i]
        #     try:
        #         if not os.path.exists(root):
        #             os.mkdir(root)
        #         if not os.path.exists(path):
        #             os.mkdir(path)
        #         with open(path + '/' + self.palces[i] + '.txt', 'w') as f:
        #             f.write(str(self.pockmon[i]))
        #     except Exception as e:
        #         print(e)
                
        # 打印宝可梦链接
        # root = './url'
        # for i in range(0, len(self.urls)):
        #     print(len(self.urls[i]))
        #     area = Traditional2Simplified(self.palces[i])
        #     try:
        #         if not os.path.exists(root):
        #             os.mkdir(root)
        #         np.savetxt(root + '/' + area + '.txt', self.urls[i], fmt='%s')
        #     except Exception as e:
        #         print(e)
        

    def get_image_address(self, id):
        if id >= len(self.palces):
            print('超出范围')
            return
        data = []
        area = Traditional2Simplified(self.palces[id])
        src = './url/' + area + '.txt'
        root = './imgsrc'
        with open(src, 'r') as f:
            urls = f.readlines()
            for url in urls:
                url = url.strip('\n')
                r = requests.get(url)
                r.encoding = r.apparent_encoding
                html = r.text
                div_bf = BeautifulSoup(html, features='html.parser')
                image = div_bf.find('a', class_='image').img
                image_address = image['data-url']
                data.append('https:' + image_address)
                print('https:' + image_address)
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            np.savetxt(root + '/' + area + '.txt', data, fmt='%s')
        except Exception as e:
            print(e)

    def get_image(self, id):
        area = Traditional2Simplified(self.palces[id])
        src = './imgsrc/' + area + '.txt'
        root = './image'
        path = root + '/' + area
        with open(src, 'r') as f:
            urls = f.readlines()
            k = 0
            for url in urls:
                address = url.strip('\n')
                name = Traditional2Simplified(self.pockmon[id][k][0])
                try:
                    if not os.path.exists(root):
                        os.mkdir(root)
                    if not os.path.exists(path):
                        os.mkdir(path)
                    if not os.path.exists(path + '/' + name + '.png'):
                        r = requests.get(address)
                        with open(path + '/' + name + '.png', 'wb') as f:
                            f.write(r.content)
                except Exception as e:
                    print(e)
                k = k + 1
        


if __name__ == "__main__":
    target = downloader()
    target.first_process()
    target.get_image(7)
    # for i in range(0,8):
    #     target.get_image(i)
