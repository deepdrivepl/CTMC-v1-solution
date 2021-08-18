import os

from glob import glob
from tqdm import tqdm

from txt2MOT import bbox_yolo2mot

'''
MOT  (absolute): <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
YOLO (relative): <cls> <xc> <yc> <wc> <hc>
'''

def json2mot(yolo_objects, out_dir, W, H, obj_id=-1, conf=-1, x=1, y=-1, z=-1):
    for fdict in tqdm(yolo_objects):
        seqdir, imdir, fname = fdict['filename'].split(os.path.sep)[-3:]
        mot_path = os.path.join(out_dir, '%s.txt' % seqdir)
        
        frame_id = int(os.path.splitext(os.path.basename(fdict['filename']))[0])
        yolo_bboxes = [[fobj['relative_coordinates']['center_x'], fobj['relative_coordinates']['center_y'], 
                        fobj['relative_coordinates']['width'], fobj['relative_coordinates']['height']]
                       for fobj in fdict['objects']]
        mot_bboxes = [bbox_yolo2mot(yolo_bbox, W, H) for yolo_bbox in yolo_bboxes]
        mot_confs = [obj['confidence'] for obj in fdict['objects']]
        mot_objects = [[frame_id, obj_id]+mot_bbox+[conf, x, y, z] for (mot_bbox, conf) in zip(mot_bboxes, mot_confs)]

        with open(mot_path, 'a') as f:
            for mot_object in mot_objects:
                f.write('%s\n' % ','.join([str(x) for x in mot_object])) 
        
        