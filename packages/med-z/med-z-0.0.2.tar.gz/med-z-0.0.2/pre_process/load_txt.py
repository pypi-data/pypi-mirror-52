import re
from pathlib import Path


def phrasing(par):
    sentences = re.split('[；;,\s]', par)
    while '' in sentences:
        sentences.remove('')
    save_as_file(sentences)
    print("文件已处理完毕！")


def save_as_file(sentences):
    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'file.yaml'
    with open(file_location, 'a+', encoding='utf8') as file_object:
        for sen in sentences:
            file_object.write('孕产次')
            file_object.write('\t')
            file_object.write(sen)
            file_object.write('\n')
