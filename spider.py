"""
模块注释
"""
import re

# 导入系统内置的模块 urllib 内的 request 对象
from urllib import request


class Spider(object):
    """
    类注释
    """
    url = 'https://www.panda.tv/cate/lol?pdt=1.24.s1.3.4bj0qcfmnof'
    # 对HTML进行根匹配模式,正则表达式的含义是没有两端的边界的非贪婪的多个所有字符
    root_pattern = '<div class="video-info">([\s\S]*?)<span class="video-station-info">'
    # 对获取的 video-info 进一步提取 video-name
    name_pattern = '</i>([\s\S]*?)</span>\s*<span class="video-number">'
    # 对获取的 video-info 进一步提取 video-number
    number_pattern = '<span class="video-number"><i class="ricon ricon-eye"></i>([\s\S]*?)</span>'
    # 定义获取内容的私有方法

    def __fetch_content(self):
        """
        方法注释
        """

        # urlopen方法：请求服务器获得HTML
        r = request.urlopen(Spider.url)
        # read方法可以把返回的r的HTML读出来，这时候的HTML不是标准格式
        htmls = r.read()
        # 使用str把 htmls 转换成指定格式的字符串
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)

        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            #  findall 返回的 name number 是列表
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)

        return anchors

    #  refine 是提炼我们得到的列表
    def __refine(self, anchors):
        #  把名字的数据进行提炼，使用方法是 对列表内内的字典元素的值进行处理，用内置函数strip提炼原字符串
        #  anchor 的结构是 {'name':['名字']， 'number':['人数']}
        l = lambda anchor: {'name': anchor['name'][0].strip(),
                            'number': anchor['number'][0]
                            }
        #  通过映射，将列表内的所有字典元素进行处理
        return map(l, anchors)

    #  sort 排序方法
    def __sort(self, anchors):
        #  系统内置 sorted函数，根据key比较大小排序，当key是函数时，sorted自动传入一个元素
        # 这里也可以用lambda代替，这样就不用定义新函数
        #  reverse参数默认是false，改为true就是降序
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    #  因为字典不能比较大小，我们要定义函数把观看人数返回
    def __sort_seed(self, anchor):
        # 用正则表达式提取人数里数字
        r = re.findall('\d*', anchor['number'])
        #  findall 返回的是列表，所以先获取返回的字符串再转浮点型
        number = float(r[0])
        # 有‘万’字的数字要转换格式
        if '万' in anchor['number']:
            number *= 10000
        return number

    #  打印排好序的主播
    def __show(self, anchors):
        #  要为已经排好序的列表添加排名
        for rank in range(0, len(anchors)):
            print('排名   '+str(rank+1)
                  +'   '+anchors[rank]['name']
                  +'   '+anchors[rank]['number'])

    # go实际是Spider的入口方法，是总控方法，所有方法的调用要汇集到go
    #  通过go的层次可以看出数据每一步的处理逻辑,多写平级函数，平铺式展示
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        #  map 返回的结果是对象，再将返回的对象转换成列表
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)

spider = Spider()
spider.go()
