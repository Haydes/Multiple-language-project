from bs4 import BeautifulSoup
import re
import pandas as pd

file = open('urls/19941614.html', 'rb')
# 19941614 c+shell
# 1359680 c#+c
html = file.read()
bs = BeautifulSoup(html,"html.parser") # 缩进格式
# print(bs.prettify()) # 格式化html结构
# print(bs.title) # 获取title标签的名称
# print(bs.title.name) # 获取title的name
# print(bs.title.string) # 获取head标签的所有内容
# print(bs.head)
# print(bs.div)  # 获取第一个div标签中的所有内容
# print(bs.div["id"]) # 获取第一个div标签的id的值
# print(bs.a)
# print(bs.find_all("a")) # 获取所有的a标签
content = bs.find(id="mainbar").text.lower()
# print(str) # 获取id="u1"
line = " c |c\+\+|python|php|c#|shell|javascript|js"
pattern = re.compile(line, re.I)
javaPattern = re.compile('java', re.I)
m = pattern.findall(content)
keywords = set()

if 'javascript' in m:
    content = content.replace('javascript', '')
javaM = javaPattern.findall(content)
if javaM.__len__() > 0:
    m.append('java')
if m.__len__() > 0:
    lowerM = ['javascript' if i == 'js' else i for i in m]
    # 关键词添加进set
    keywords = set.union(keywords, set(lowerM))
print(1)
# for item in bs.find_all("a"):
#     print(item.get("href")) # 获取所有的a标签，并遍历打印a标签中的href的值
# for item in bs.find_all("a"):
#     print(item.get_text())