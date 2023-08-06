import time
import re
import os

# paragraph = "子宫下段剖宫产；孕次5产次1 孕39周 枕左前剖宫产；巨大儿；胎膜早破；\
# 高龄初产妇妊娠监督；足月单活胎；"


def phrasing(par):
    sentences = re.split('[；;,\s]', par)
    while '' in sentences:
        sentences.remove('')
    return sentences

# sen_list = phrasing(paragraph)

def save_sens(sen_list):
    path = os.path.abspath('.')
    print(path)
    with open(path + '/show_data.txt', 'w', encoding='utf8') as file_object:
        for sen in sen_list:
            file_object.write('孕产次')
            file_object.write('\t')
            file_object.write(sen)
            file_object.write('\n')
#print("结束于：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# save_sens(sen_list)

print("OK")
