
  
def line_intersect_line(line1, line2):
    '''
    line1 : tuple
        tuple of tuple defining a line segment: ( (x1,y1), (x2,y2) )
    line2 : tuple
        tuple of tuple defining a line segment: ( (x1,y1), (x2,y2) )
    ''' 
      
    class Point: 
        def __init__(self, xy): 
            self.x = xy[0] 
            self.y = xy[1]
    
    # Given three colinear points p, q, r, the function checks if  
    # point q lies on line segment 'pr'  
    def on_segment(p, q, r): 
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
            return True
        return False
    
    def orientation(p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Colinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise
        
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
        # for details of below formula.
        
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0): 
            # Clockwise orientation
            return 1
        elif (val < 0): 
            # Counterclockwise orientation
            return 2
        else: 
            # Colinear orientation
            return 0

    p1 = Point(line1[0])
    q1 = Point(line1[1])
    p2 = Point(line2[0])
    q2 = Point(line2[1])

    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)):
        return True
  
    # Special Cases 
  
    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
    if ((o1 == 0) and on_segment(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
    if ((o2 == 0) and on_segment(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
    if ((o3 == 0) and on_segment(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
    if ((o4 == 0) and on_segment(p2, q1, q2)): 
        return True
  
    # If none of the cases
    return False

def rect_intersect_line(rect, line):
    '''
    assumes frame oriented rect

    Attributes
    ---------
    rect : list-like
        list of rectangle coord in ltrb format
    line : list-like
        line defined by 2 points in x1,y1,x2,y2 format
    '''
    line_x1, line_y1, line_x2, line_y2 = line 
    del_x = float(line_x2 - line_x1)
    del_y = float(line_y2 - line_y1)
    if del_x != 0:
        m =  del_y / del_x
        c = line_y1 - m*line_x1
    else:
        m = None
        c = None

    line_min_y, line_max_y = sorted([line_y1, line_y2])
    line_min_x, line_max_x = sorted([line_x1, line_x2])

    l,t,r,b = rect

    if line_min_y > b or line_max_y < t or line_min_x > r or line_max_x < l: # early return
        return False

    # Check intersection with rect verticals
    if not (line_min_y > b or line_max_y < t ): # line segment even lie within the t & b of rect

        if m is None: # line is vertical
            if l == line_max_x:
                return True
            elif r == line_max_y:
                return True
        else: # line is horizontal or diagonal
            ## Check intersection with rect left
            left_y_point = m * l + c
            if t <= left_y_point <= b and line_min_y <= left_y_point <= line_max_y and line_min_x <= l <= line_max_x:
                return True 

            ## Check intersection with rect right
            right_y_point = m * r + c
            if t <= right_y_point <= b and line_min_y <= right_y_point <= line_max_y and line_min_x <= r <= line_max_x:
                return True 

    # Check intersection with rect horizontals
    if not (line_min_x > r or line_max_x < l): # line segment even lie within the l & r of rect
        
        ## Check intersection with rect top
        if m == 0: # line is horizontal
            if t == line_max_y:
                return True
        if m is None: # line is vertical
            top_x_point = line_x1
        else: # line is diagonal
            top_x_point = ( t - c ) / m
        if l <= top_x_point <= r and line_min_x <= top_x_point <= line_max_x and line_min_y <= t <= line_max_y:
            return True 

        ## Check intersection with rect bot
        if m == 0: # line is horizontal
            if b == line_max_y:
                return True
        else:
            if m is None: # line is vertical 
                bot_x_point = line_x1
            else: # line is diagonal
                bot_x_point = ( b - c ) / m
        if l <= bot_x_point <= r and line_min_x <= bot_x_point <= line_max_x and line_min_y <= b <= line_max_y:
            return True 

    return False


if __name__ == "__main__":
    import numpy as np
    import cv2

    line1 = ((0,5), (100,80))
    line2 = ((0,12), (100,12))
    line3 = ((0,100), (100,90))

    sketchboard = np.zeros((100,100))
    cv2.line(sketchboard, line1[0], line1[1], (255,255,255))
    cv2.line(sketchboard, line2[0], line2[1], (255,255,255))
    cv2.line(sketchboard, line3[0], line3[1], (255,255,255))
    cv2.imshow('', sketchboard)
    cv2.waitKey(0)

    assert line_intersect_line(line1, line2)
    assert not line_intersect_line(line1, line3)
