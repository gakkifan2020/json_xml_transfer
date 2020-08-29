# coding: utf-8
import glob
import pandas as pd
import xml.etree.ElementTree as ET

classes = ["person","hat"]


def xml_to_csv(path):
    train_list = []
    eval_list = []

    for cls in classes:
        xml_list = []
        # 读取注释文件
        for xml_file in glob.glob(path + '/*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall('object'):
                if cls == member[0].text:
                    value = (root.find('filename').text,
                             int(root.find('size')[0].text),
                             int(root.find('size')[1].text),
                             member[0].text,
                             float(member[4][0].text),
                             float(member[4][1].text),
                             float(member[4][2].text),
                             float(member[4][3].text)
                             )
                    xml_list.append(value)

        for i in range(0, int(len(xml_list) * 0.9)):
            train_list.append(xml_list[i])
        for j in range(int(len(xml_list) * 0.9) + 1, int(len(xml_list))):
            eval_list.append(xml_list[j])

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    # 保存为CSV格式
    train_df = pd.DataFrame(xml_list, columns=column_name)
    eval_df = pd.DataFrame(eval_list, columns=column_name)
    train_df.to_csv('/home/chenxin/models-master/research/object_detection/images/data/train531.csv', index=None)
    eval_df.to_csv('/home/chenxin/models-master/research/object_detection/images/data/eval531.csv', index=None)


def main():
    # path = 'E:\\\data\\\Images'
    path = r'/home/chenxin/models-master/research/object_detection/images/train531'  # path参数更具自己xml文件所在的文件夹路径修改
    xml_to_csv(path)
    print('Successfully converted xml to csv.')


main()