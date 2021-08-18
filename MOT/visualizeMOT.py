import argparse
import os

from glob import glob
from tqdm import tqdm

import cv2
import numpy as np
import PIL.ImageColor as ImageColor

'''
python visualizeMOT.py --imgs_dir CTMC-v1-Cufix-solution/train --img_mot --mot_dir CTMC-v1-Cufix-solution/results/norfair/data --out_dir CTMC-v1-Cufix-solution/results/norfair/data/vis
'''

STANDARD_COLORS = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]

def visualize_bbox(img, bbox, class_name, color, thickness=1):
    color = color[::-1]
    bbox = [int(x) for x in bbox]
    xmin, ymin, w, h = bbox
    cv2.rectangle(img, (xmin, ymin), (xmin+w, ymin+h), color=color, thickness=thickness)
    
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    cv2.rectangle(img, (xmin, ymin), (xmin + text_width, ymin + int(1.5 * text_height)), color, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(xmin, ymin + int(1.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35, 
        color=(0,0,0), 
        lineType=cv2.LINE_AA,
    )
    return img

def visualize_dir(img_dir, out_dir, mot_path, palette, padding):
    anns = [x.rstrip().split(',')[:7] for x in open(mot_path)]
    anns = [list(map(float, lst)) for lst in anns]
    imgs = sorted(glob(os.path.join(img_dir, '*.jpg')))
    
    for path in imgs:
        img_id = int(os.path.basename(os.path.splitext(path)[0]))
        img_objs = [x for x in anns if x[0]==img_id]
        img = cv2.imread(path)
            
        for img_obj in img_objs:
            frame, obj_id, xmin, ymin, w, h, conf = img_obj
            name = '%04d (%0.2f)' % (obj_id, conf)
            img = visualize_bbox(img, [xmin-padding, ymin-padding, w+padding, h+padding], name, palette[int(obj_id % len(palette))], thickness=1)

        cv2.imwrite(os.path.join(out_dir, os.path.basename(path)), img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgs_dir', type=str, required=True)
    parser.add_argument('--img_mot', default=False, action='store_true')
    parser.add_argument('--mot_dir', type=str, required=True)
    parser.add_argument('--out_dir', type=str, required=True)
    parser.add_argument('--padding', type=int, default=0, required=False)
    args = parser.parse_args()

    palette = [ImageColor.getrgb(color) for color in STANDARD_COLORS]

    if args.img_mot:
        img_dirs = glob(os.path.join(args.imgs_dir, '*', 'img1'))
        seqs = [x.split(os.sep)[-2] for x in img_dirs]
    else:
        img_dirs = glob(os.path.join(args.imgs_dir, '*'))
        seqs = [x.split(os.sep)[-1] for x in img_dirs]

    for img_dir, seq in tqdm(zip(img_dirs, seqs)):
        mot_path = os.path.join(args.mot_dir, '%s.txt' % seq)
        if not os.path.isfile(mot_path):
            print('%s does not exist!' % mot_path)
            continue

        out_dir = os.path.join(args.out_dir, seq)
        os.makedirs(out_dir, exist_ok=True)
        visualize_dir(img_dir, out_dir, mot_path, palette, args.padding)