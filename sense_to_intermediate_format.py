import sys
import os
from zipfile import ZipFile
from io import StringIO
import json
import shutil


def build_ground_truth_string(image_path, text, buffer: StringIO):
    _template = "{image_path}\t{text}\n"
    buffer.write(_template.format(image_path=image_path, text=text)) 

def main(dataset_path, output_dir):
    buf = StringIO()
    with ZipFile(dataset_path, 'r') as zf:
        for file in zf.namelist():
            if not file.endswith('.json'): continue
            labels = json.load(zf.open(file))['labels']
            for label in labels:
                try:
                    gt_text = label['annotations']['Tattoo']['data']
                    gt_text = gt_text.upper()
                    gt_text = gt_text.replace(' ', '')
                    gt_text = gt_text.replace('5', 'X')
                    if len(gt_text) < 4 or len(gt_text) > 4: continue

                    image_path = label['path']
                    output_image_path = os.path.join(output_dir, 'test', os.path.basename(image_path))
                    with open(output_image_path, 'wb') as fp:
                        fp.write(zf.open(image_path).read())
                except:
                    continue

                build_ground_truth_string(os.path.join('test', os.path.basename(image_path)), gt_text, buf)
    
    with open(os.path.join(output_dir, 'gt.txt'), 'w') as fp:
        fp.write(buf.getvalue())

if __name__ == '__main__':
    try:
        dataset_path = sys.argv[1]
    except:
        raise ValueError('Supply a path to a sense dataset')

    output_dir = os.path.join('dataset', os.path.basename(dataset_path).split('.')[0])
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test'), exist_ok=True)
    main(dataset_path, output_dir)
