import os
class Pinyin():
    #汉字转拼音方法
    def getpinyin(self,hanzi):  
        result=""  
        for i in hanzi:
            #将汉字转换为unicode编码
            code = str(i.encode('unicode_escape')) 
            # print(code) # b'\\u4f60'
            #截取后 4F60
            val = code[-5:-1].upper()
            #初始化字典
            dict={}
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'pinyincode.txt')
            with open(data_path) as f:
                for item in f.readlines():
                    #填充数据到字典中
                    dict[item.split()[0]]=item.split()[1].strip()[:-1]
            #如多个汉字转换通过"-"分隔
            result+=dict[val].lower()+"-"
        return result[:-1] 

p=Pinyin()
print(p.getpinyin("你好"))