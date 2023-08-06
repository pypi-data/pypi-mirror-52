import re


def phrasing(par):
    sentences = re.split('[；;,\s]', par)
    while '' in sentences:
        sentences.remove('')
    save_as_file(sentences)
    print("文件已处理完毕！")


def save_as_file(sentences):
    with open('../data/show_data.txt', 'a+', encoding='utf8') as file_object:
        for sen in sentences:
            file_object.write('孕产次')
            file_object.write('\t')
            file_object.write(sen)
            file_object.write('\n')
