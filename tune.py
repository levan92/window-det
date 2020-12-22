import json
import argparse
from pathlib import Path

from pprint import pprint
import cv2
import numpy as np

from windet import WindowDetector

ap = argparse.ArgumentParser()
ap.add_argument('--config', help='Config file', required=True)
ap.add_argument('--pos', help='Positive input image')
ap.add_argument('--neg', help='Negative input image')
ap.add_argument('--out', help='Tuning output json file', default='configs/tuning.json')
args = ap.parse_args()

config_path = Path(args.config)
windowDetector = WindowDetector.from_json(config_path)

# Reading positive image
pos_imgpath = Path(args.pos)
assert pos_imgpath.is_file()
pos_img = cv2.imread(str(pos_imgpath))
img_height, img_width = pos_img.shape[:2]
max_dim = max(img_height, img_width)
area = img_height * img_width

# Reading negative image
neg_imgpath = Path(args.neg)
assert neg_imgpath.is_file()
neg_img = cv2.imread(str(neg_imgpath))

# Initial window detection
pos_show_img = windowDetector.tune(pos_img)
neg_show_img = windowDetector.tune(neg_img)

# Concat outputs to show
img_show = np.concatenate((pos_show_img, neg_show_img), axis=1)
show_window = 'Window Detector Tuning'
cv2.namedWindow(show_window, cv2.WINDOW_NORMAL)

cv2.resizeWindow(show_window, 1920, 1080)

# Trackbars for respective tunable parameters

def update_hough_min_line_length(value):
    global img_show
    windowDetector.hough_min_line_length = value
    pos_show_img = windowDetector.tune(pos_img)
    neg_show_img = windowDetector.tune(neg_img)
    img_show = np.concatenate((pos_show_img, neg_show_img), axis=1)
cv2.createTrackbar('hough_min_line_length',show_window, windowDetector.hough_min_line_length, max_dim, update_hough_min_line_length)

def update_hough_max_line_gap(value):
    global img_show
    windowDetector.hough_max_line_gap = value
    pos_show_img = windowDetector.tune(pos_img)
    neg_show_img = windowDetector.tune(neg_img)
    img_show = np.concatenate((pos_show_img, neg_show_img), axis=1)
cv2.createTrackbar('hough_max_line_gap',show_window,windowDetector.hough_max_line_gap,max_dim, update_hough_max_line_gap)

def update_hough_thresh(value):
    global img_show
    windowDetector.hough_thresh = value
    pos_show_img = windowDetector.tune(pos_img)
    neg_show_img = windowDetector.tune(neg_img)
    img_show = np.concatenate((pos_show_img, neg_show_img), axis=1)
cv2.createTrackbar('hough_thresh',show_window,windowDetector.hough_thresh, 500, update_hough_thresh)

# before_tuning = f'{Path(args.out).parent / Path(args.out).stem}-orig.jpg'
# cv2.imwrite(before_tuning, img_show)

while True:
    cv2.imshow(show_window, img_show)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

final_tune_dict = {
    'hough_min_line_length': cv2.getTrackbarPos('hough_min_line_length', show_window),
    'hough_max_line_gap': cv2.getTrackbarPos('hough_max_line_gap', show_window),
    'hough_thresh': cv2.getTrackbarPos('hough_thresh', show_window),
}

cv2.destroyAllWindows()

print('Final tuning values:')
pprint(final_tune_dict)
print(f'Dumped to {args.out}')
with open(args.out,'w') as f:
    json.dump(final_tune_dict, f)

# tuning_img_path = f'{Path(args.out).parent / Path(args.out).stem}-tuned.jpg'
# cv2.imwrite(tuning_img_path, img_show)