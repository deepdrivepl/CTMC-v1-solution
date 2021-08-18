import os

from glob import glob
from tqdm import tqdm

'''
MOT  (absolute): <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
YOLO (relative): <cls> <xc> <yc> <wc> <hc>
'''

def bbox_yolo2mot(yolo_bbox, W, H):
    xc,yc,w,h = [float(x) for x in yolo_bbox]
    xc,yc = xc*W, yc*H
    w,h   = int(w*W), int(h*H)
    xmin, ymin = int(xc-0.5*w), int(yc-0.5*h)
    if xmin < 0:
        xmin=0
    if ymin < 0:
        ymin=0
    if (xmin+w) > W:
        w = W - xmin
    if (ymin+h) > H:
        h = H - ymin

    return [xmin, ymin, w, h]
    
    
def txt2mot(txt_dir, mot_path, W, H, obj_id=-1, conf=-1, x=1, y=-1, z=-1, ext='txt'):
    txt_files = sorted(glob(os.path.join(txt_dir, '*.%s' % ext)))
    
    mot_objects_all=[]
    for txt_file in tqdm(txt_files):
        frame_id = int(os.path.splitext(os.path.basename(txt_file))[0])
        
        yolo_objects = [x.rstrip().split(' ') for x in open(txt_file)]
        yolo_bboxes = [x[1:] for x in yolo_objects]
        mot_bboxes = [bbox_yolo2mot(yolo_bbox, W, H) for yolo_bbox in yolo_bboxes if len(yolo_bbox)!=0]
        
        mot_objects = [[frame_id, obj_id]+mot_bbox+[conf, x, y, z] for mot_bbox in mot_bboxes]
        mot_objects_all+=mot_objects
    
    mot_objects.sort(key=lambda x: x[0])
    with open(mot_path, 'w') as f:
        for mot_object in mot_objects_all:
            f.write('%s\n' % ','.join([str(x) for x in mot_object])) 