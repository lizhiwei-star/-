import pandas as pd
import numpy as np
import pymysql
import re
from pyecharts  import Line,Pie

coon = pymysql.connect(
    host='localhost', user='root', passwd='',
    port=3306, db='fff', charset='utf8'
    # port必须写int类型
    # charset必须写utf8，不能写utf-8
    )
cursor = coon.cursor()
sql='select image,cast(price as char)price,cast(deal as char)deal,cast(commit_num as char)commit_num,cast(shop as char)shop,cast(location as char)location from jd'
df=pd.read_sql(sql=sql,con=coon)
#print(df.values)
df=pd.DataFrame(df)
# df=df.drop('id',axis=1)
print(pd.isnull(df).values.any())
print('去重之前的形状',df.shape)
df=df.drop_duplicates(keep='first')
print('去重之后的形状',df.shape)
print(df.head())

#######
#对commit_num进行处理，转换为float类型
#######
def get_buy_num(buy_num):
    if u'万' in buy_num:  # 针对1-2万/月或者10-20万/年的情况，包含-
        buy_num=float(buy_num.replace("万",''))*10000
        #print(buy_num)
    else:
        buy_num=float(buy_num)
    return buy_num

df['location'] = df['location'].replace('','未知')
#fillna("['未知']")datasets = pd.DataFrame()
for index, row in df.iterrows():
    #print(row["place"])
    row["location"] = row["location"]    
    row["commit_num"]=get_buy_num(row["commit_num"][:-3].replace('+',''))
    print(row["location"],row["commit_num"])

df.to_csv('taobao_food.csv',encoding='utf8',index_label=False)

#####
#生成云图
#####
import pandas as pd
import jieba, re
import matplotlib.pyplot as plt
from wordcloud  import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
fr = open(r'D:\python\Fonts\stopwords1893.txt', 'r')
stop_word_list = fr.readlines()
new_stop_word_list = []
for stop_word in stop_word_list:
    stop_word = stop_word.replace('\\ufeef', '').strip() 
    new_stop_word_list.append(stop_word)
file1 = df.loc[:,'deal'].dropna(how='any')  # 去掉空值
print('去掉空值后有{}行'.format(file1.shape[0]))  # 获得一共有多少行
print(file1.head())
text1 = ''.join(i for i in file1)  # 把所有字符串连接成一个长文本
responsibility = re.sub(re.compile(r'，|；|\.|、|。|\n'), '', text1)  # 去掉逗号等符号
wordlist1 = jieba.cut(responsibility, cut_all=True)
print(wordlist1)
word_dict={}
word_list=''

for word in wordlist1:
    if (len(word) > 1  and not word in new_stop_word_list):
        word_list = word_list + ' ' + word
        if (word_dict.get(word)):
            word_dict[word] = word_dict[word] + 1
        else:
            word_dict[word]=1
       
print(word_list)
print(word_dict)#输出每个关键词字出现次数

#按次数进行排序
sort_words=sorted(word_dict.items(),key=lambda x:x[1],reverse=True)
print(sort_words[0:101])#输出前0-100的词

font_path=r'C:\Windows\Fonts\SIMYOU.TTF'

#bgimg=imread(r'1.png')#设置背景图片
wc = WordCloud(font_path=font_path,  # 设置字体
               background_color="black",  # 背景颜色               
               max_words=300,  # 词云显示的最大词数               
            #    stopwords=stopwords,  # 设置停用词               
               max_font_size=400,  # 字体最大值              
               random_state=42,  # 设置有多少种随机生成状态，即有多少种配色               
               width=2000, height=1720,                
               margin=4,  # 设置图片默认的大小,margin为词语边缘距离              
               ).generate(str(word_list))
#image_colors = ImageColorGenerator(bgimg)  # 根据图片生成词云颜色
plt.imshow(wc)
plt.axis("off")
plt.savefig("examples.jpg")  # 必须在plt.show之前，不是图片空白
plt.show()

#####
#生成折线图和饼状图进行分析
#####
def status(location,price,percent):
    if '自营' in location:
        self_managment = '京东自营'
        if len(percent) ==0:
            percent.append(price)
        else :
            percent[0]=percent[0] + price
    else:
        self_managment = "其他"
        if len(percent) ==1:
            percent.append(price)
        else :
            percent[1]=percent[1] + price
    return percent
print(df['commit_num'].sort_values(ascending=False))
print(df.loc[df['commit_num'].sort_values(ascending=False).index,'shop'])
a=df['commit_num'].sort_values(ascending=False)
b=df.loc[df['commit_num'].sort_values(ascending=False).index,'shop']
c=df.loc[df['commit_num'].sort_values(ascending=False).index,'deal']
frames = [a,b,c]
data=pd.concat(frames,axis=1)
print(data)
a=df['commit_num'].sort_values(ascending=False)
b=df.loc[df['commit_num'].sort_values(ascending=False).index,'shop']
c=df.loc[df['commit_num'].sort_values(ascending=False).index,'location']
frames = [a,b,c]
data=pd.concat(frames,axis=1)
print(data)

a=df.loc[df['commit_num'].sort_values(ascending=False).index,'price']
b=df['commit_num'].sort_values(ascending=False)
frames = [a,b]
data=pd.concat(frames,axis=1).reset_index()
print('商品价格对销售额的影响分析',data)

bar = Line("商品价格对销售额的影响分析")
bar.add("价格随销量降低而变化",data['price'].index,data['commit_num'], is_smooth=True,mark_line=["max", "average"])
bar.render('折线图1.html')
# row["self_managment"]=get_buy_num(row["location"])
percent=[]
for index, row in df.iterrows():
    #print(row["place"])
    row["location"] = row["location"]    
    status(row["location"],row["commit_num"],percent)
    print(row["location"],row["commit_num"])
pie = Pie("商品价格对销售额的影响分析")
pie.add("京东销售",['自营','其他'],percent, is_smooth=True,mark_line=["max", "average"])
pie.render('饼状图.html')