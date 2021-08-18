import argparse
import os
import json

from glob import glob

from txt2MOT import txt2mot
from json2MOT import json2mot


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--out_dir', type=str, required=True)
    parser.add_argument('--json', default=False, action='store_true')
    parser.add_argument('--width', type=int, default=400)
    parser.add_argument('--height', type=int, default=320)
    args = parser.parse_args()
    print(args)
    
    os.makedirs(args.out_dir, exist_ok=True)
    
    W, H = args.width, args.height
    if not args.json:
        seq_paths = sorted(glob(os.path.join(args.input, '*')))
        for seq_path in seq_paths:
            seq = seq_path.split(os.sep)[-1]
            yolo_dir = os.path.join(seq_path, 'img1')
            mot_path = os.path.join(args.out_dir, '%s.txt' % seq)
            txt2mot(yolo_dir, mot_path, W, H)
    else:
        try:
            yolo_objects = json.load(open(args.input))
        except:
            print('%s does not exist!' % args.input)
        else:
            json2mot(yolo_objects, args.out_dir, W, H)
    
    
    