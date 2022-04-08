import math

def find_angle(p1, p2, p3):
    (x1, y1) = p1
    (x2, y2) = p2
    (x3, y3) = p3
    
    # 使用三角函数公式获取3个点p1-p2-p3，以p2为角的角度值，0-180度之间
    angle = int(math.degrees(math.atan2(y1-y2, x1-x2) - math.atan2(y3-y2, x3-x2)))
    '''if angle < 0:
        angle = angle + 360
    if angle > 180:
        angle = 360 - angle'''
    
    return angle


# 判断actor是否被到objects列表里的任意一个角色
def is_touch(actor, objects):
    for obj in objects:
        if actor.colliderect(obj):
            return True
    return False