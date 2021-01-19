import json

import cv2
import numpy as np

from utils import line_intersect_line, rect_intersect_line

class WindowDetector():
    def __init__(self, 
                 target_window_pegs=None,
                 target_window_areas=None,
                 canny_min_val=150, canny_max_val=500, closing_kernel_width=5,
                 hough_rho=1, hough_theta_degree=1, hough_thresh=100,
                 hough_min_line_length=1000, hough_max_line_gap=500):
        '''
        target_window_pegs : list (optional)
            list of line segments in tuples of tuples ((X1,Y1),(X2,Y2)) format.
            If none is given, all lines are considered window.

        target_window_areas : list (optional)
            list of rectangular areas in LTRB tuples.
            If none is given, all lines are considered window.

        '''

        self.target_window_pegs = target_window_pegs
        if self.target_window_pegs is not None:
            assert self.target_window_pegs

        self.target_window_areas = target_window_areas
        if self.target_window_areas is not None:
            assert self.target_window_areas

        # Canny Edge Detector
        self.canny_min_val = canny_min_val
        self.canny_max_val = canny_max_val

        # Closing
        self.closing_kernel = np.ones((closing_kernel_width, closing_kernel_width), np.uint8)

        # Hough Transform (getting lines)
        self.hough_rho = hough_rho
        self.hough_theta = hough_theta_degree * np.pi / 180
        self.hough_thresh = hough_thresh
        self.hough_min_line_length = hough_min_line_length
        self.hough_max_line_gap = hough_max_line_gap

    @classmethod
    def from_json(cls, json_path):
        with open(json_path, 'r')  as f:
            config = json.load(f)
        return cls(**config)

    def get_edges_map(self, img):
        return cv2.Canny(img, self.canny_min_val, self.canny_max_val)

    def closing(self, edges_map):
        return cv2.morphologyEx(edges_map, cv2.MORPH_CLOSE, self.closing_kernel)

    def lines_from_edges(self, edges_map):
        return cv2.HoughLinesP(edges_map,
                                rho = self.hough_rho,
                                theta = self.hough_theta,
                                threshold = self.hough_thresh,
                                minLineLength=self.hough_min_line_length,
                                maxLineGap=self.hough_max_line_gap,
                                )

    def get_lines(self, img):    
        edges_map = self.get_edges_map(img)
        closed_edges_map = self.closing(edges_map)
        lines = self.lines_from_edges(closed_edges_map)
        return lines

    def has_target_windows(self, img):
        lines = self.get_lines(img)
        if lines is None:
            return False

        if self.target_window_areas is None and self.target_window_pegs is None:
            return len(lines) > 0
        
        if self.target_window_pegs is not None:
            for line_seg in self.target_window_pegs:
                for line in lines:
                    if line_intersect_line(line, line_seg):
                        break
                else: # None of the lines intersect with this peg
                    return False

        if self.target_window_areas is not None:
            for rect in self.target_window_areas:
                for line in lines:
                    line_flat = line.flatten()
                    if rect_intersect_line(rect, line_flat):
                        break
                else: # None of the lines intersect with this rect
                    return False

        return True

    def tune(self, img):
        img_show = img.copy()

        lines = self.get_lines(img)

        if lines is None:
            # print('No lines')
            return img_show
        # print(f'Num lines: {len(lines)}')

        line_color = (255, 255, 0)
        intersect_color = (0, 255, 0)
        no_intersect_color = (0, 255, 255)

        # if self.target_window_areas is None:
        for line in lines:
            line_flat = line.flatten()
            x1, y1, x2, y2 = line_flat
            cv2.line(img_show, (x1, y1), (x2, y2), line_color, 2)

        if self.target_window_areas is not None:
            for rect in self.target_window_areas:
                # intersect = False
                rcolor = no_intersect_color
                for line in lines:
                    line_flat = line.flatten()
                    if rect_intersect_line(rect, line_flat):
                        # x1, y1, x2, y2 = line_flat
                        # cv2.line(img_show, (x1, y1), (x2, y2), line_color, 2)
                        # intersect = True
                # if intersect:
                       rcolor = intersect_color
                # else: 
                    # rcolor = no_intersect_color
                l, t, r, b = rect
                cv2.rectangle(img_show, (l, t), (r, b), rcolor, 2)

        return img_show
