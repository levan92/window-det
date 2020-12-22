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