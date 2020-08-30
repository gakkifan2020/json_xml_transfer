import json
import numpy as np
import os
import xml.etree.cElementTree as ET
from tqdm import tqdm
import argparse
import cv2

DATA_TYPE = 'train'
ROOT_DIR = 'my_data'
if DATA_TYPE == 'train':
    FILE_DIR = './%s/train/' % ROOT_DIR
    TXT_TYPE = 'train'

elif DATA_TYPE == 'val':
    FILE_DIR = './%s/val/' % ROOT_DIR
    TXT_TYPE = 'v
else:
    raise ValueError('No type matched!')

with open("./my_data/mchar_%s.json" % DATA_TYPE, 'r') as f:  # read json file
    json_file = json.load(f)
    json_dict = dict(json_file)
    print(json_dict["000000.png"])


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_base_path', type=str, default='./%s/' % ROOT_DIR)
    args = parser.parse_args()
    return args


def conver_json2txt():
    args = arg_parser()
    save_path = args.save_base_path + TXT_TYPE + '.txt'
    with open(save_path, mode='w') as fp:
        for idx, pic_file in tqdm(enumerate(os.listdir(FILE_DIR))):
            img = cv2.imread(FILE_DIR + pic_file)
            pic_anno = json_dict[pic_file]
            if idx % 100 == 0:
                print(idx, pic_file)
            lines = ''
            lines += str(idx)
            lines += ' ' + './data/%s/%s/' % (ROOT_DIR, DATA_TYPE) + pic_file
            lines += ' ' + str(img.shape[1]) + ' ' + str(img.shape[0])  # first width then height
            for i in range(len(pic_anno["height"])):
                x_min = int(pic_anno["left"][i])
                y_min = int(pic_anno["top"][i])
                x_max = int(pic_anno["left"][i] + pic_anno["width"][i])
                y_max = int(pic_anno["top"][i] + pic_anno["height"][i])
                # lines += ' ' + str(json_dict['shapes'][i]['label'])
                lines += ' ' + str(pic_anno["label"][i])
                lines += ' ' + str(x_min) + ' ' + str(y_min) + ' ' + str(x_max) + ' ' + str(y_max)
            lines += '\n'
            fp.writelines(lines)

        print('finish')


if __name__ == "__main__":
    conver_json2txt()
