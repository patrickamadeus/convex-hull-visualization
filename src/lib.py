# simple point to line distance finder
def dist_pt_line(p1,p2,pt):
    A,B,C = (p2[1] - p1[1]) , (p1[0] - p2[0]) , (p1[0]*(p1[1] - p2[1]) + p1[1]*(p2[0] - p1[0]))
    return abs(A*pt[0] + B*pt[1] + C)/((A**2 + B**2)**(0.5))

def linear_value(p1,p2,pt):
    A,B,C = (p2[1] - p1[1]) , (p1[0] - p2[0]) , (p1[0]*(p1[1] - p2[1]) + p1[1]*(p2[0] - p1[0]))
    return A*pt[0] + B*pt[1] + C

# convex hull algorithm from array of points
def convex_hull(points, p1 = None, p2 = None , types = 0):
    # base condition
    if len(points) == 0:
        return []
    if len(points) == 1:
        return [points[0]]
    
    # initial 2 areas separation
    if p1 == None and p2 == None:
        p_min , p_max = points[0] , points[-1]
        
        upper,lower = [],[]
        for point in points:
            if linear_value(p_min,p_max,point) < 0:
                upper.append(point)
            elif linear_value(p_min,p_max,point) > 0:
                lower.append(point)
        return [p_min] + convex_hull(upper,p_min,p_max,1) + [p_max] + convex_hull(lower,p_min,p_max,-1)

    #find the maximum distance point
    distance, p_max = 0, None
    for point in points:
        if dist_pt_line(p1,p2,point) > distance:
            distance = dist_pt_line(p1,p2,point)
            p_max = point
    
    left,right = [],[]
    for point in points:
        if linear_value(p1,p_max,point) * types < 0:
            left.append(point)
        if linear_value(p_max,p2,point) * types < 0:
            right.append(point)

    if types == 1:
        return convex_hull(left , p1 , p_max, types) + [p_max] + convex_hull(right , p_max , p2, types)
    else:
        return convex_hull(right , p_max , p2, types) + [p_max] + convex_hull(left , p1 , p_max, types)