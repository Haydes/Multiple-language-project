import numpy as np
import pandas as pd
import wget
import re
import openpyxl
from itertools import combinations
import time
import urllib
import os
from bs4 import BeautifulSoup

def allCombination():
    # c++ '+'在正则表达式里需要转义
    # c 前后保留一个空格防止太多误匹配
    languages = np.array([" c ", "c++", "python", "java", "php", "c#", "shell", "javascript"])
    for n in range(2, 9):
        filename = "tuple-" + str(n) + ".txt"
        f = open('tuples/' + filename, 'w')
        for i in combinations(languages, n):
            line = ""
            for k in range(n-1):
                line += i[k] + "|"
            line += i[n-1]
            f.write(line)
            f.write("\n")
        f.close()

def readRawData():
    sheet_names = ["JAVA+PYTHON", "JAVA+C", "PYTHON+C", "JAVA+PHP", "PYTHON+PHP", "PHP+C", "C#+PYTHON", "C#+JAVA", "C#+C",
                   "C#+PHP", "PYTHON+SHELL", "JAVA+SHELL", "PHP+SHELL", "C+SHELL", "C#+SHELL", "JavaScript+JAVA", "JavaScript+C",
                   "JavaScript+PYTHON", "JavaScript+C++", "JavaScript+PHP", "JavaScript+SHELL", "JavaScript+C#", "C+C++",
                   "JAVA+C++", "PYTHON+C++", "PHP+C++", "C#+C++", "SHELL+C++"]

    # test case
    # sheet_names = ["JAVA+PYTHON"]

    data = None
    i = 1
    for sheet_name in sheet_names:
        print("reading sheet " + str(i) + "...")
        i = i + 1
        df = pd.read_excel("raw data.xlsx", sheet_name=sheet_name)
        if data is None:
            data = df
        else:
            data = pd.concat([data, df], ignore_index=True)
    return data


def read3AndMoreCombineData():
    sheet_name = "morethan3"
    data = None
    df = pd.read_excel("raw data.xlsx", sheet_name=sheet_name)
    if data is None:
        data = df
    else:
        data = pd.concat([data, df], ignore_index=True)
    return data



# use wget to download post
def downloadPosts(data):
    total = data.shape[0]
    for index, r in data.iterrows():
        filename = 'urls/' + str(r.id) + '.html'
        # wget.download(r.link, out=filename)
        dir = os.path.abspath('.')
        work_path = os.path.join(dir, filename)
        try:
            urllib.request.urlretrieve(r.link, work_path)
        except urllib.error.HTTPError as e:
            print(e.reason)
        print("progress: " + str(index + 1) + "/" + str(total))
        if (index+1)%200 == 0:
            time.sleep(120)

# 对于post文件，只考虑内容部分 <div id="mainbar" role="main">
# 对于output部分，所有的同一个tuple放在同一个文件下，每条数据添加一列表示它当前的语言组合
# 思路：只遍历一遍，pattern为8combination，然后记录匹配的语言个数，放在对应的dataframe里（2~8分7个dataframe）
# 也要添加raw data中，2-tuple以外的所有post进本地文件，一起分析
def classification(data: pd.DataFrame):
    data.rename(columns={'view': 'view_num'}, inplace=True)

    # js 后加空格防止匹配到json之类的
    combineLine = " c |c\+\+|python|php|c#|shell|javascript|js "

    # 不同dataFrame输出不同文件
    outputFrame2 = pd.DataFrame(columns=['id', 'title', 'vote', 'answer', 'view_num', 'link', 'time', 'author', 'reputation', 'combination'])
    outputFrame3 = outputFrame2
    outputFrame4 = outputFrame2
    outputFrame5 = outputFrame2
    outputFrame6 = outputFrame2
    outputFrame7 = outputFrame2
    outputFrame8 = outputFrame2


    # 通过该语言组合作为正则表达式，忽略大小写
    pattern = re.compile(combineLine, re.I)
    # java单独匹配，每次都需要先匹配完js才考虑java
    javaPattern = re.compile('java', re.I)
    # 遍历data中的每一行数据
    for index, r in data.iterrows():
        postID = 'urls/' + str(r.id) + '.html'
        # 打开该行数据对应的文件
        postFile = open(postID, 'rb')
        postHtml = postFile.read()
        bs = BeautifulSoup(postHtml, "html.parser")  # 缩进格式
        # 找到该html文件里<div id="mainbar">的内容并小写化
        content = bs.find(id="mainbar").text.lower()
        keywords = set()

        # content里符合pattern的所有匹配集合
        m = pattern.findall(content)
        if 'javascript' in m:
            # 先把匹配到的javascript去掉
            content = content.replace('javascript', '')
        javaM = javaPattern.findall(content)
        if javaM.__len__() > 0:
            m.append('java')

        # 集合不为空
        if m.__len__() > 0:
            # 所有js替换为javascript
            m = ['javascript' if i == 'js ' else i for i in m]
            # 关键词添加进set
            keywords = set.union(keywords, set(m))
            # 对所有关键词进行排序
            sortedKeywords = sorted(list(keywords))
            # keyword string
            kwStr = "|".join(sortedKeywords).replace(" c ", "c").replace("java ", "java")
            # 把当前组合入这条数据r
            r['combination'] = kwStr
            # 把r写入对应dataframe
            if sortedKeywords.__len__() == 2:
                outputFrame2 = outputFrame2.append(r, ignore_index=True)
            elif sortedKeywords.__len__() == 3:
                outputFrame3 = outputFrame3.append(r, ignore_index=True)
            elif sortedKeywords.__len__() == 4:
                outputFrame4 = outputFrame4.append(r, ignore_index=True)
            elif sortedKeywords.__len__() == 5:
                outputFrame5 = outputFrame5.append(r, ignore_index=True)
            elif sortedKeywords.__len__() == 6:
                outputFrame6 = outputFrame6.append(r, ignore_index=True)
            elif sortedKeywords.__len__() == 7:
                outputFrame7 = outputFrame7.append(r, ignore_index=True)
            elif sortedKeywords.__len__() == 8:
                outputFrame8 = outputFrame8.append(r, ignore_index=True)
            else:
                print('sortedKeywords.__len__ < 2 or >8 branch: ' + str(r.id) + ' ' + r.link)
                continue

            print('grouping progress: ' + str(index+1) + '/' + str(data.shape[0]))
        else:
            print('m.__len__ else brach: ' + str(r.id) + ' ' + r.link)
    # # 符合的数据写入excel
    path = 'excels/grouped data.xlsx'
    wb = openpyxl.load_workbook(path)
    excelWriter = pd.ExcelWriter(path, engine='openpyxl')
    excelWriter.book = wb


    # 这里写进excel
    outputFrame2.to_excel(excelWriter, sheet_name="2 tuple", index=None)
    outputFrame3.to_excel(excelWriter, sheet_name="3 tuple", index=None)
    outputFrame4.to_excel(excelWriter, sheet_name="4 tuple", index=None)
    outputFrame5.to_excel(excelWriter, sheet_name="5 tuple", index=None)
    outputFrame6.to_excel(excelWriter, sheet_name="6 tuple", index=None)
    outputFrame7.to_excel(excelWriter, sheet_name="7 tuple", index=None)
    outputFrame8.to_excel(excelWriter, sheet_name="8 tuple", index=None)
    excelWriter.save()
    excelWriter.close()


# allCombination()
# downloadPosts(data)
data1 = readRawData()
data2 = read3AndMoreCombineData()
data = pd.concat([data1, data2], ignore_index=True)
classification(data)

