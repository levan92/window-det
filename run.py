import json
import argparse
import warnings
from pathlib import Path

import cv2
import numpy as np

from windet import WindowDetector

ap = argparse.ArgumentParser()
ap.add_argument('--config', help='Config file', required=True)
ap.add_argument('--output', help='Output file', required=True)
input_group = ap.add_mutually_exclusive_group(required=True)
input_group.add_argument('--image', help='Input image (either image or dir input required)')
input_group.add_argument('--dir', help='Input directory of images (either image or dir input required)')
args = ap.parse_args()

config_path = Path(args.config)
windowDetector = WindowDetector.from_json(config_path)

results = []
if args.image:
    print('Running on single image.')
    imgpath = Path(args.image)
    assert imgpath.is_file()
    img = cv2.imread(str(imgpath))
    res = windowDetector.has_target_windows(img)
    results.append((str(imgpath),res))
    if res:
        print('Image has target windows.')
    else:
        print('Image does not have target windows.')
elif args.dir:
    print('Running through all images in given folder.')
    dirpath = Path(args.dir)
    assert dirpath.is_dir()
    for imgpath in dirpath.glob('*'):
        if imgpath.suffix in ('.jpg','.png','.jpeg'):
            img = cv2.imread(str(imgpath))
            res = windowDetector.has_target_windows(img)
            results.append((str(imgpath),res))
        else:
            warnings.warn(f'Path does not have an image extension: {imgpath}')

with open(args.output,'w') as f:
    for l in results:
        f.write(f'{l[0]},{l[1]}\n')