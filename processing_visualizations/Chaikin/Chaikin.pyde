global points, state

def setup():
    size(400, 400)
    global points, state
    points = [[50, height - 50], [width / 2, 85], [width - 50, height - 50], [50, height - 50]]
    state = 0 # Three state: Current, Precut, AfterCut
    

def draw():
    background(255)
    pushStyle()
    fill(0)
    textSize(13)
    textAlign(CENTER)
    text("Depth = " + str(int(state / 3)), width/2, 35)
    popStyle()
    if state % 3 in [0, 1]:
        draw_P()
    if state % 3 == 1:
        draw_QR()
    if state % 3 == 2:
        global points, state
        state += 1
        points = cut_corner(points)
        draw_P()
            

def draw_P():
    pushStyle()
    fill(0)
    stroke(0)
    for i, p in enumerate(points):
        x, y = p
        if i > 0:
            x_, y_ = points[i-1]
            strokeWeight(1)
            line(x_, y_, x, y)
        ellipse(x, y, 5, 5)
        if i != len(points) - 1:
            textSize(13 - int(state/3) * 2)
            textAlign(CENTER)
            text("P" + str(i), x, y - 15)
    popStyle()
        
def draw_QR():
    new_points = cut_corner(points)
    pushStyle()
    fill(0, 200, 0)
    stroke(0, 200, 0)
    for i, p in enumerate(new_points):
        x, y = p
        if i > 0:
            x_, y_ = new_points[i-1]
            strokeWeight(1)
            line(x_, y_, x, y)
        ellipse(x, y, 5, 5)
        textSize(13 - int(state/3) * 2)
        textAlign(CENTER)
        if i % 2 == 0 and i != len(new_points) - 1:
            text("Q" + str(i/2), x, y - 15)
        if i % 2 == 1:
            text("R" + str(i/2), x, y - 15)
    x, y = new_points[0]
    x_, y_ = new_points[-1]
    line(x_, y_, x, y)
    popStyle()
    

def cut_corner(points, depth=1, factor=4):
    """ Chaikin's corner cutting algorithm

    :param points: points of the polygon
    :param depth: num of cuts
    :param factor: cutting factor
    :return: points of smoothed polygon
    """
    for d in range(depth):
        new_points = []
        for i in range(len(points) - 1):
            pi_x, pi_y = points[i]
            pj_x, pj_y = points[i + 1]
            qi_x = pi_x * (factor - 1) / factor + pj_x / factor
            qi_y = pi_y * (factor - 1) / factor + pj_y / factor
            ri_x = pi_x / factor + pj_x * (factor - 1) / factor
            ri_y = pi_y / factor + pj_y * (factor - 1) / factor
            new_points += [[qi_x, qi_y], [ri_x, ri_y]]
        points = new_points
        points += [points[0]]
    return points

def mousePressed():
    saveFrame("./output/#####.jpg")
    global state
    state += 1
